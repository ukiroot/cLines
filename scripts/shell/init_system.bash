#!/bin/bash

set -o xtrace
set -o verbose
set -o errexit

#Initializations of varibles
DIR_MAIN=$(dirname `readlink -e "$0"`)
VM_ISO="/var/lib/libvirt/images/VyOS.iso"
VYOS_URL="https://github.com/vyos/vyos-rolling-nightly-builds/releases/download/1.5-rolling-202402291036/vyos-1.5-rolling-202402291036-amd64.iso"
#Max value for NUMBER_OF_EUT is 9
NUMBER_OF_EUT="8"
EUT_BRIDGE="eut_bridge"
BRIDGE_RESOURCE_MASK="mighty_bridge_"
LINUXCHCHAN=(
    "ursamajor" \
    "ursaminor" \
    "lupus" \
    "virgo" \
    "vulpecula" \
    "aquarius" \
    "aries" \
    "pisces"
)


#Initializations of functions
function install_python_packages_via_apt {
apt -y install \
    python3 \
    python3-pip \
    python3-virtualenv \
    pep8
}


function install_system_packages_via_apt {
apt -y install \
    telnet \
    virt-manager
}


function delete_bridge {
    MASK="$1"
    ip link show type bridge | grep ": ${MASK}" | awk '{print $2}' | sed 's/://' | while read BRIDGE; do
        ip link del dev "${BRIDGE}"
    done
}


function init_bridge_interfaces {
    delete_bridge "${BRIDGE_RESOURCE_MASK}"
    delete_bridge "${EUT_BRIDGE}"
    ip link add name "${EUT_BRIDGE}" type bridge
    ip link set dev "${EUT_BRIDGE}" up
}


function create_eut_config {
    VM_NAME="EUT_${VM_ID}"
    VM_DISK="/var/lib/libvirt/images/${VM_NAME}.qcow2"
    MAC_1="52:54:00:9e:5d:${VM_ID}2"
    MAC_2="52:54:00:c5:8c:${VM_ID}3"
    MAC_3="52:54:00:24:c0:${VM_ID}4"
    MAC_4="52:54:00:dd:ba:${VM_ID}5"
    CONSOLE_PORT="700${VM_ID}"

    rm -fv "${VM_DISK}"
    qemu-img create -f qcow2 "${VM_DISK}" 2048M # Unfortunately since VyOS 1.2.X  requires a total of at least 2000MB to properly install.
    virsh list --all | grep " ${VM_NAME} " | while read NAME; do
    if [ "`echo ${NAME} | grep running | awk '{print $2}'`" = "${VM_NAME}" ]; then
        virsh destroy "${VM_NAME}"
    fi
    virsh undefine "${VM_NAME}"
    done
    cat > /etc/libvirt/qemu/${VM_NAME}.xml << EOF
<domain type='kvm'>
    <name>${VM_NAME}</name>
    <uuid>14a0a55f-83b9-4917-a2da-7${VM_ID}7${VM_ID}7${VM_ID}7${VM_ID}7${VM_ID}7${VM_ID}</uuid>
    <memory unit='KiB'>524288</memory>
    <currentMemory unit='KiB'>524288</currentMemory>
    <vcpu placement='static'>1</vcpu>
    <os>
        <type arch='x86_64' machine='pc-i440fx-2.8'>hvm</type>
    </os>
    <features>
        <acpi/>
        <apic/>
        <vmport state='off'/>
    </features>
    <cpu mode='custom' match='exact'>
        <model fallback='allow'>kvm64</model>
    </cpu>
    <clock offset='utc'>
        <timer name='rtc' tickpolicy='catchup'/>
        <timer name='pit' tickpolicy='delay'/>
        <timer name='hpet' present='no'/>
    </clock>
    <on_poweroff>destroy</on_poweroff>
    <on_reboot>restart</on_reboot>
    <on_crash>restart</on_crash>
    <pm>
        <suspend-to-mem enabled='no'/>
        <suspend-to-disk enabled='no'/>
    </pm>
    <devices>
        <emulator>/usr/bin/kvm</emulator>
        <disk type='file' device='disk'>
          <driver name='qemu' type='qcow2'/>
          <source file='${VM_DISK}'/>
          <target dev='hda' bus='ide'/>
          <boot order='1'/>
          <address type='drive' controller='0' bus='0' target='0' unit='0'/>
        </disk>
        <disk type='file' device='cdrom'>
          <driver name='qemu' type='raw'/>
          <source file='${VM_ISO}'/>
          <target dev='hdb' bus='ide'/>
          <readonly/>
          <boot order='2'/>
          <address type='drive' controller='0' bus='0' target='0' unit='1'/>
        </disk>
        <controller type='usb' index='0' model='ich9-ehci1'>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x7'/>
        </controller>
        <controller type='usb' index='0' model='ich9-uhci1'>
          <master startport='0'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0' multifunction='on'/>
        </controller>
        <controller type='usb' index='0' model='ich9-uhci2'>
          <master startport='2'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x1'/>
        </controller>
        <controller type='usb' index='0' model='ich9-uhci3'>
          <master startport='4'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x2'/>
        </controller>
        <controller type='pci' index='0' model='pci-root'/>
        <controller type='ide' index='0'>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>
        </controller>
        <controller type='virtio-serial' index='0'>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
        </controller>
        <interface type='bridge'>
          <mac address='${MAC_1}'/>
          <source bridge='${EUT_BRIDGE}'/>
          <model type='rtl8139'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
        </interface>
        <interface type='bridge'>
          <mac address='${MAC_2}'/>
          <source bridge='${EUT_BRIDGE}'/>
          <model type='rtl8139'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
        </interface>
        <interface type='bridge'>
          <mac address='${MAC_3}'/>
          <source bridge='${EUT_BRIDGE}'/>
          <model type='rtl8139'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
        </interface>
        <interface type='bridge'>
          <mac address='${MAC_4}'/>
          <source bridge='${EUT_BRIDGE}'/>
          <model type='rtl8139'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x08' function='0x0'/>
        </interface>
        <serial type='tcp'>
          <source mode='bind' host='0.0.0.0' service='${CONSOLE_PORT}'/>
          <protocol type='telnet'/>
          <target port='0'/>
        </serial>
        <console type='tcp'>
          <source mode='bind' host='0.0.0.0' service='${CONSOLE_PORT}'/>
          <protocol type='telnet'/>
          <target type='serial' port='0'/>
        </console>
        <input type='mouse' bus='ps2'/>
        <input type='keyboard' bus='ps2'/>
        <memballoon model='virtio'>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
        </memballoon>
    </devices>
</domain>
EOF
}


function linuxchan_hostname_hack {
    DIR_FOR_IMAGE="/var/lib/libvirt/images/min_dist/"
    IMAGE_NAME="linuxchan.img"
    IMAGE="${DIR_FOR_IMAGE}${IMAGE_NAME}"
    DISK_DEV=""
    DISK_DEV_SECTION="p1"
    DIR_CHROOT="/mnt/debian"

    DISK_DEV=`losetup -f --show "${IMAGE}"`
    partprobe "${DISK_DEV}"
    mount -v "${DISK_DEV}${DISK_DEV_SECTION}" "${DIR_CHROOT}"
    mount -v --bind /dev "${DIR_CHROOT}/dev"
    mount -vt devpts devpts "${DIR_CHROOT}/dev/pts"
    mount -vt proc proc "${DIR_CHROOT}/proc"
    mount -vt sysfs sysfs "${DIR_CHROOT}/sys"
    mount -vt tmpfs tmpfs "${DIR_CHROOT}/run"

    cat > "${DIR_CHROOT}/etc/grub.d/40_custom" << "EOF"
#!/bin/sh
exec tail -n +3 $0
EOF
    cat > "${DIR_CHROOT}/etc/rc.local" << "EOF"
#!/bin/sh -e
HOSTNAME=`cat /proc/cmdline | grep -oE 'hostname=[a-z0-9\\-]+' | sed 's/hostname=//'`
if [ "${HOSTNAME}" != '' ]; then
    /bin/hostname "${HOSTNAME}"
fi
exit 0
EOF
    cat > "${DIR_CHROOT}/root/grub_cutomize.sh" << EOF
LINUXCHCHAN=(${LINUXCHCHAN[@]})
EOF
    cat >> "${DIR_CHROOT}/root/grub_cutomize.sh" << "EOF"
seq 8 | while read VM_ID; do
    HOSTNAME=${LINUXCHCHAN[$(( ${VM_ID} - 1 ))]}
    cat /boot/grub/grub.cfg | grep -A20 "menuentry 'Debian GNU/Linux'" | grep -B 20 '^}' | \
    sed -e 's/Debian GNU\/Linux/'${HOSTNAME}'/' -e 's/console=ttyS0/console=ttyS0 net.ifnames=0 biosdevname=0 hostname='${HOSTNAME}'/' >> /etc/grub.d/40_custom
done
update-grub2
EOF
    chroot "${DIR_CHROOT}" /bin/bash -c "chmod +x /etc/rc.local"
    chroot "${DIR_CHROOT}" /bin/bash /root/grub_cutomize.sh
    chroot "${DIR_CHROOT}" /bin/bash -c "rm -fv /root/grub_cutomize.sh"



    umount -v "${DIR_CHROOT}/dev/pts"
    umount -v "${DIR_CHROOT}/dev"
    umount -v "${DIR_CHROOT}/proc"
    umount -v "${DIR_CHROOT}/sys"
    umount -v "${DIR_CHROOT}/run"
    umount -v "${DIR_CHROOT}"
    losetup -d "${DISK_DEV}"
}


function create_linuxchan_config {
    MAC_1="52:54:00:9e:77:${VM_ID}7"
    MAC_2="52:54:00:c5:77:${VM_ID}8"
    CONSOLE_PORT="770${VM_ID}"

    virsh list --all | grep " ${VM_NAME} " | while read NAME; do
    if [ "`echo ${NAME} | grep running | awk '{print $2}'`" = "${VM_NAME}" ]; then
        virsh destroy "${VM_NAME}"
    fi
    virsh undefine "${VM_NAME}"
    done
    cat > /etc/libvirt/qemu/${VM_NAME}.xml << EOF
<domain type='kvm'>
    <name>${VM_NAME}</name>
    <uuid>14a0a55f-83b9-4917-7777-7${VM_ID}7${VM_ID}7${VM_ID}7${VM_ID}7${VM_ID}7${VM_ID}</uuid>
    <memory unit='KiB'>524288</memory>
    <currentMemory unit='KiB'>524288</currentMemory>
    <vcpu placement='static'>1</vcpu>
    <os>
        <type arch='x86_64' machine='pc-i440fx-2.8'>hvm</type>
    </os>
    <features>
        <acpi/>
        <apic/>
        <vmport state='off'/>
    </features>
    <cpu mode='custom' match='exact'>
        <model fallback='allow'>kvm64</model>
    </cpu>
    <clock offset='utc'>
        <timer name='rtc' tickpolicy='catchup'/>
        <timer name='pit' tickpolicy='delay'/>
        <timer name='hpet' present='no'/>
    </clock>
    <on_poweroff>destroy</on_poweroff>
    <on_reboot>restart</on_reboot>
    <on_crash>restart</on_crash>
    <pm>
        <suspend-to-mem enabled='no'/>
        <suspend-to-disk enabled='no'/>
    </pm>
    <devices>
        <emulator>/usr/bin/kvm</emulator>
        <disk type='file' device='disk'>
          <driver name='qemu' type='raw'/>
          <source file='/var/lib/libvirt/images/min_dist/linuxchan.img'/>
          <target dev='sda' bus='sata'/>
          <boot order='1'/>
          <shareable/>
          <address type='drive' controller='0' bus='0' target='0' unit='0'/>
        </disk>
        <controller type='usb' index='0' model='ich9-ehci1'>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x7'/>
        </controller>
        <controller type='usb' index='0' model='ich9-uhci1'>
          <master startport='0'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0' multifunction='on'/>
        </controller>
        <controller type='usb' index='0' model='ich9-uhci2'>
          <master startport='2'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x1'/>
        </controller>
        <controller type='usb' index='0' model='ich9-uhci3'>
          <master startport='4'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x2'/>
        </controller>
        <controller type='pci' index='0' model='pci-root'/>
        <controller type='ide' index='0'>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>
        </controller>
        <controller type='virtio-serial' index='0'>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
        </controller>
        <interface type='bridge'>
          <mac address='${MAC_1}'/>
          <source bridge='${EUT_BRIDGE}'/>
          <model type='rtl8139'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
        </interface>
        <interface type='bridge'>
          <mac address='${MAC_2}'/>
          <source bridge='${EUT_BRIDGE}'/>
          <model type='rtl8139'/>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
        </interface>
        <serial type='tcp'>
          <source mode='bind' host='0.0.0.0' service='${CONSOLE_PORT}'/>
          <protocol type='telnet'/>
          <target port='0'/>
        </serial>
        <console type='tcp'>
          <source mode='bind' host='0.0.0.0' service='${CONSOLE_PORT}'/>
          <protocol type='telnet'/>
          <target type='serial' port='0'/>
        </console>
        <input type='mouse' bus='ps2'/>
        <input type='keyboard' bus='ps2'/>
        <memballoon model='virtio'>
          <address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
        </memballoon>
    </devices>
</domain>
EOF
}


function get_vyos {
    wget -O "${VM_ISO}" "${VYOS_URL}"
}


install_python_packages_via_apt
install_system_packages_via_apt

get_vyos

seq "${NUMBER_OF_EUT}" | while read VM_ID; do
    create_eut_config
done

bash "${DIR_MAIN}/bootstrap_linuxchan.bash"
linuxchan_hostname_hack
seq "${NUMBER_OF_EUT}" | while read VM_ID; do
    VM_NAME=${LINUXCHCHAN[$(( ${VM_ID} - 1 ))]}
    create_linuxchan_config
done

init_bridge_interfaces

systemctl reload libvirtd
