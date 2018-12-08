#!/bin/bash

set -o xtrace
set -o verbose
set -o errexit

DIR_FOR_IMAGE="/var/lib/libvirt/images/min_dist/"
IMAGE_NAME="linuxchan.img"
IMAGE="${DIR_FOR_IMAGE}${IMAGE_NAME}"
DISK_DEV="/dev/loop0"
DISK_DEV_SECTION="p1"
DISK_DEV_1="${DISK_DEV}${DISK_DEV_SECTION}"
DEBIAN_VER="stretch"
DIR_CHROOT="/mnt/debian"

apt-get install -y \
    debootstrap \
    qemu-utils
mkdir -p "${DIR_FOR_IMAGE}"
cd "${DIR_FOR_IMAGE}"
rm -f "${IMAGE}"
qemu-img create "${IMAGE}" 1G
rmmod loop || true
modprobe loop max_part=15
losetup "${DISK_DEV}" "${IMAGE}"
fdisk "${DISK_DEV}" << "EOF"
n
p
1


a
w
EOF
partprobe "${DISK_DEV}"
sleep 5
mkfs.ext4 "${DISK_DEV_1}"
mkdir -p "${DIR_CHROOT}"
mount -v "${DISK_DEV_1}" "${DIR_CHROOT}"
debootstrap --verbose --include=sudo,locales,nano,wget,grub-pc --arch amd64 "${DEBIAN_VER}" "${DIR_CHROOT}" http://www.nic.funet.fi/debian/
cat > "${DIR_CHROOT}/etc/fstab" << "EOF"
/dev/sda1       /               ext4        defaults        0       1
EOF
cat > "${DIR_CHROOT}/etc/apt/sources.list" << EOF
deb http://www.nic.funet.fi/debian ${DEBIAN_VER} main contrib non-free
deb-src http://www.nic.funet.fi/debian ${DEBIAN_VER} main contrib non-free

deb http://www.nic.funet.fi/debian/ ${DEBIAN_VER}-updates main contrib non-free
deb-src http://www.nic.funet.fi/debian/ ${DEBIAN_VER}-updates main contrib non-free

deb http://www.nic.funet.fi/debian/ ${DEBIAN_VER}-backports main contrib non-free
deb-src http://www.nic.funet.fi/debian/ ${DEBIAN_VER}-backports main contrib non-free

deb http://www.nic.funet.fi/debian-security ${DEBIAN_VER}/updates main contrib non-free
deb-src http://www.nic.funet.fi/debian-security ${DEBIAN_VER}/updates main contrib non-free
EOF

cat > "${DIR_CHROOT}/root/postinst.sh" << EOF
#!/bin/bash

apt-get update
tzselect << "OEF"
8
39
2
1
OEF
TZ='Europe/Moscow'; export TZ
useradd -m -s /bin/bash tester
passwd tester << "OEF"
tester
tester
OEF
passwd << "OEF"
admin
admin
OEF
cat > /etc/default/locale << OEF
LANG=en_US.UTF-8
OEF
cat > /etc/locale.gen << OEF
en_US.UTF-8 UTF-8
OEF
locale-gen
apt-get -y install linux-image-amd64 firmware-linux firmware-ralink firmware-realtek firmware-atheros ssh
apt-get clean
sed -i 's/^#GRUB_TERMINAL.*/GRUB_TERMINAL="serial console"/' /etc/default/grub
sed -i 's/^GRUB_CMDLINE_LINUX.*/GRUB_CMDLINE_LINUX="console=ttyS0"/' /etc/default/grub
grub-install "${DISK_DEV}" --modules="biosdisk part_msdos"
update-grub2
sed -i 's/\/dev\/'"${DISK_DEV_1}"'/\/dev\/sda1/g' /boot/grub/grub.cfg
sync
EOF

mount -v --bind /dev "${DIR_CHROOT}/dev"
mount -vt devpts devpts "${DIR_CHROOT}/dev/pts"
mount -vt proc proc "${DIR_CHROOT}/proc"
mount -vt sysfs sysfs "${DIR_CHROOT}/sys"
mount -vt tmpfs tmpfs "${DIR_CHROOT}/run"
chroot "${DIR_CHROOT}" /bin/bash /root/postinst.sh
chroot "${DIR_CHROOT}" /bin/bash -c "rm -fv /root/postinst.sh"
umount -v "${DIR_CHROOT}/dev/pts"
umount -v "${DIR_CHROOT}/dev"
umount -v "${DIR_CHROOT}/proc"
umount -v "${DIR_CHROOT}/sys"
umount -v "${DIR_CHROOT}/run"
umount -v "${DIR_CHROOT}"
losetup -d "${DISK_DEV}"
