#!/bin/bash

set -o xtrace
set -o verbose
set -o errexit


if [ false ]; then
fdisk /dev/sdb << "EOF"
n
p
1


a
1
w
EOF
mkfs.ext4 /dev/sdb1
mkdir /mnt/debian
mount -v /dev/sdb1 /mnt/debian

debootstrap --verbose --include=sudo,locales,nano,wget,grub-pc --arch amd64 stretch /mnt/debian http://ftp.ru.debian.org/debian/


cat > /mnt/debian/etc/fstab << "EOF"
/dev/sda1       /               ext4        defaults        0       1
EOF

cat > /mnt/debian/etc/apt/sources.list << "EOF"
deb http://ftp.ru.debian.org/debian stretch main contrib non-free
deb-src http://ftp.ru.debian.org/debian stretch main contrib non-free

deb http://ftp.debian.org/debian/ stretch-updates main contrib non-free
deb-src http://ftp.debian.org/debian/ stretch-updates main contrib non-free

deb http://ftp.debian.org/debian/ stretch-backports main contrib non-free
deb-src http://ftp.debian.org/debian/ stretch-backports main contrib non-free

deb http://ftp.ru.debian.org/debian-security stretch/updates main contrib non-free
deb-src http://ftp.ru.debian.org/debian-security stretch/updates main contrib non-free
EOF



cat > /mnt/debian/root/postinst.sh << "EOF"
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

apt-get -y install linux-image-amd64
apt-get -y install firmware-linux firmware-ralink firmware-realtek firmware-atheros ssh qemu-kvm libvirt-daemon libvirt-daemon-system curl wpasupplicant
apt-get clean

sed -i 's/^#GRUB_TERMINAL.*/GRUB_TERMINAL="serial console"/' /etc/default/grub
sed -i 's/^GRUB_CMDLINE_LINUX.*/GRUB_CMDLINE_LINUX="console=ttyS0"/' /etc/default/grub

update-grub2
grub-install /dev/sdb --modules="biosdisk part_msdos"
sed -i 's/\/dev\/sdb1/\/dev\/sda1/g' /boot/grub/grub.cfg
sync
EOF


mount -v --bind /dev /mnt/debian/dev
mount -vt devpts devpts /mnt/debian/dev/pts
mount -vt proc proc /mnt/debian/proc
mount -vt sysfs sysfs /mnt/debian/sys
mount -vt tmpfs tmpfs /mnt/debian/run


chroot /mnt/debian /bin/bash /root/postinst.sh
chroot /mnt/debian /bin/bash -c "rm -rf /root/postinst.sh"


umount -v /mnt/debian/dev/pts
umount -v /mnt/debian/dev
umount -v /mnt/debian/proc
umount -v /mnt/debian/sys
umount -v /mnt/debian/run


umount -v /mnt/debian/
fi
