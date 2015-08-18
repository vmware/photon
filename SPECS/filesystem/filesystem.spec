Summary:	Default file system
Name:		filesystem
Version:	7.5
Release:	8%{?dist}
License:	GPLv3
Group:		System Environment/Base
Vendor:		VMware, Inc.
URL:		http://www.linuxfromscratch.org
Distribution:	Photon
%description
The filesystem package is one of the basic packages that is installed
on a Linux system. Filesystem contains the basic directory
layout for a Linux operating system, including the correct permissions
for the directories. This version is for a system configured with systemd.
%prep
%build
%install
#
#	6.5.  Creating Directories
#
install -vdm 755 %{buildroot}/{dev,proc,run/{media/{floppy,cdrom},lock},sys}
install -vdm 755 %{buildroot}/{boot,etc/{opt,sysconfig},home,mnt}
install -vdm 755 %{buildroot}/etc/systemd/network
install -vdm 755 %{buildroot}/{var}
install -dv -m 0750 %{buildroot}/root
install -dv -m 1777 %{buildroot}/tmp %{buildroot}/var/tmp
install -vdm 755 %{buildroot}/usr/{,local/}{bin,include,lib,sbin,src}
install -vdm 755 %{buildroot}/usr/{,local/}share/{color,dict,doc,info,locale,man}
install -vdm 755 %{buildroot}/usr/{,local/}share/{misc,terminfo,zoneinfo}
install -vdm 755 %{buildroot}/usr/libexec
install -vdm 755 %{buildroot}/usr/{,local/}share/man/man{1..8}
install -vdm 755 %{buildroot}/etc/profile.d

ln -svfn usr/lib %{buildroot}/lib
ln -svfn usr/bin %{buildroot}/bin
ln -svfn usr/sbin %{buildroot}/sbin
ln -svfn run/media %{buildroot}/media

#	Symlinks for AMD64
%ifarch x86_64
	ln -svfn usr/lib %{buildroot}/lib64
	ln -svfn lib %{buildroot}/usr/lib64
	ln -svfn ../lib %{buildroot}/usr/local/lib64
%endif
install -vdm 755 %{buildroot}/var/{log,mail,spool,mnt,srv}

ln -svfn var/srv %{buildroot}/srv
ln -svfn ../run %{buildroot}/var/run
ln -svfn ../run/lock %{buildroot}/var/lock
install -vdm 755 %{buildroot}/var/{opt,cache,lib/{color,misc,locate},local}
install -vdm 755 %{buildroot}/mnt/cdrom
install -vdm 755 %{buildroot}/mnt/hgfs
ln -svfn var/opt %{buildroot}/opt

#
#	6.6. Creating Essential Files and Symlinks
#
ln -svfn /proc/self/mounts %{buildroot}/etc/mtab
#touch -f %{buildroot}/etc/mtab

touch %{buildroot}/var/log/{btmp,lastlog,wtmp}
#
#	Configuration files
#
cat > %{buildroot}/etc/passwd <<- "EOF"
root::0:0:root:/root:/bin/bash
bin:x:1:1:bin:/dev/null:/bin/false
daemon:x:6:6:Daemon User:/dev/null:/bin/false
messagebus:x:18:18:D-Bus Message Daemon User:/var/run/dbus:/bin/false
systemd-bus-proxy:x:72:72:systemd Bus Proxy:/:/bin/false
systemd-journal-gateway:x:73:73:systemd Journal Gateway:/:/bin/false
systemd-journal-remote:x:74:74:systemd Journal Remote:/:/bin/false
systemd-journal-upload:x:75:75:systemd Journal Upload:/:/bin/false
systemd-network:x:76:76:systemd Network Management:/:/bin/false
systemd-resolve:x:77:77:systemd Resolver:/:/bin/false
systemd-timesync:x:78:78:systemd Time Synchronization:/:/bin/false
nobody:x:99:99:Unprivileged User:/dev/null:/bin/false
EOF
cat > %{buildroot}/etc/group <<- "EOF"
root:x:0:
bin:x:1:daemon
sys:x:2:
kmem:x:3:
tape:x:4:
tty:x:5:
daemon:x:6:
floppy:x:7:
disk:x:8:
lp:x:9:
dialout:x:10:
audio:x:11:
video:x:12:
utmp:x:13:
usb:x:14:
cdrom:x:15:
adm:x:16:
messagebus:x:18:
systemd-journal:x:23:
input:x:24:
mail:x:34:
lock:x:54:
dip:x:30:
systemd-bus-proxy:x:72:
systemd-journal-gateway:x:73:
systemd-journal-remote:x:74:
systemd-journal-upload:x:75:
systemd-network:x:76:
systemd-resolve:x:77:
systemd-timesync:x:78:
nogroup:x:99:
users:x:100:audio
sudo:x:27:
wheel:x:28:
EOF
#
#	7.2.2. Creating Network Interface Configuration Files"
#
cat > %{buildroot}/etc/systemd/network/10-dhcp-en.network <<- "EOF"
[Match]
Name=*

[Network]
DHCP=yes
EOF
#
#	7.3. Customizing the /etc/hosts File"
#
cat > %{buildroot}/etc/hosts <<- "EOF"
# Begin /etc/hosts (network card version)

127.0.0.1	localhost

# End /etc/hosts (network card version)
EOF
#
#	7.8. Configuring the system hostname
#
echo "HOSTNAME=photon.eng.vmware.com" > %{buildroot}/etc/sysconfig/network
#
#	7.9. Configuring the setclock Script"
#
cat > %{buildroot}/etc/sysconfig/clock <<- "EOF"
# Begin /etc/sysconfig/clock

UTC=1

# Set this to any options you might need to give to hwclock,
# such as machine hardware clock type for Alphas.
CLOCKPARAMS=

# End /etc/sysconfig/clock
EOF
#
#	7.10. Configuring the Linux Console"
#
cat > %{buildroot}/etc/sysconfig/console <<- "EOF"
# Begin /etc/sysconfig/console
#       Begin /etc/sysconfig/console
#       KEYMAP="us"
#       FONT="lat1-16 -m utf8"
#       FONT="lat1-16 -m 8859-1"
#       KEYMAP_CORRECTIONS="euro2"
#       UNICODE="1"
#       LEGACY_CHARSET="iso-8859-1"
# End /etc/sysconfig/console
EOF
#
#	7.13. The Bash Shell Startup Files
#
cat > %{buildroot}/etc/profile <<- "EOF"
# Begin /etc/profile
# Written for Beyond Linux From Scratch
# by James Robertson <jameswrobertson@earthlink.net>
# modifications by Dagmar d'Surreal <rivyqntzne@pbzpnfg.arg>

# System wide environment variables and startup programs.

# System wide aliases and functions should go in /etc/bashrc.  Personal
# environment variables and startup programs should go into
# ~/.bash_profile.  Personal aliases and functions should go into
# ~/.bashrc.

# Functions to help us manage paths.  Second argument is the name of the
# path variable to be modified (default: PATH)
pathremove () {
        local IFS=':'
        local NEWPATH
        local DIR
        local PATHVARIABLE=${2:-PATH}
        for DIR in ${!PATHVARIABLE} ; do
                if [ "$DIR" != "$1" ] ; then
                  NEWPATH=${NEWPATH:+$NEWPATH:}$DIR
                fi
        done
        export $PATHVARIABLE="$NEWPATH"
}

pathprepend () {
        pathremove $1 $2
        local PATHVARIABLE=${2:-PATH}
        export $PATHVARIABLE="$1${!PATHVARIABLE:+:${!PATHVARIABLE}}"
}

pathappend () {
        pathremove $1 $2
        local PATHVARIABLE=${2:-PATH}
        export $PATHVARIABLE="${!PATHVARIABLE:+${!PATHVARIABLE}:}$1"
}

export -f pathremove pathprepend pathappend

# Set the initial path
export PATH=$PATH:/bin:/usr/bin

if [ $EUID -eq 0 ] ; then
        pathappend /sbin:/usr/sbin
        unset HISTFILE
fi

# Setup some environment variables.
export HISTSIZE=1000
export HISTIGNORE="&:[bf]g:exit"

# Set some defaults for graphical systems
export XDG_DATA_DIRS=/usr/share/
export XDG_CONFIG_DIRS=/etc/xdg/

# Setup a red prompt for root and a green one for users.
NORMAL="\[\e[0m\]"
RED="\[\e[1;31m\]"
GREEN="\[\e[1;32m\]"
if [[ $EUID == 0 ]] ; then
  PS1="$RED\u@\h [ $NORMAL\w$RED ]# $NORMAL"
else
  PS1="$GREEN\u@\h [ $NORMAL\w$GREEN ]\$ $NORMAL"
fi

for script in /etc/profile.d/*.sh ; do
        if [ -r $script ] ; then
                . $script
        fi
done

unset script RED GREEN NORMAL

# End /etc/profile
EOF
#
#	7.14. Creating the /etc/inputrc File
#
cat > %{buildroot}/etc/inputrc <<- "EOF"
# Begin /etc/inputrc
# Modified by Chris Lynn <roryo@roryo.dynup.net>

# Allow the command prompt to wrap to the next line
set horizontal-scroll-mode Off

# Enable 8bit input
set meta-flag On
set input-meta On

# Turns off 8th bit stripping
set convert-meta Off

# Keep the 8th bit for display
set output-meta On

# none, visible or audible
set bell-style none

# All of the following map the escape sequence of the value
# contained in the 1st argument to the readline specific functions
"\eOd": backward-word
"\eOc": forward-word

# for linux console
"\e[1~": beginning-of-line
"\e[4~": end-of-line
"\e[5~": beginning-of-history
"\e[6~": end-of-history
"\e[3~": delete-char
"\e[2~": quoted-insert

# for xterm
"\eOH": beginning-of-line
"\eOF": end-of-line

# for Konsole
"\e[H": beginning-of-line
"\e[F": end-of-line

# End /etc/inputrc
EOF
#
#	8.2. Creating the /etc/fstab File
#
cat > %{buildroot}/etc/fstab <<- "EOF"
#	Begin /etc/fstab
#	hdparm -I /dev/sda | grep NCQ --> can use barrier
#system		mnt-pt		type		options			dump fsck
/dev/sda1	/		    ext4	    defaults,barrier,noatime,noacl,data=ordered 1 1
/dev/cdrom      /mnt/cdrom      iso9660     ro,noauto              0   0
# /dev/sda2	swap		swap		pri=1			0 0
#	mount points
#	End /etc/fstab
EOF
#
#	8.3.2. Configuring Linux Module Load Order
#
install -vdm 755 %{buildroot}/etc/modprobe.d
cat > %{buildroot}/etc/modprobe.d/usb.conf <<- "EOF"
# Begin /etc/modprobe.d/usb.conf

install ohci_hcd /sbin/modprobe ehci_hcd ; /sbin/modprobe -i ohci_hcd ; true
install uhci_hcd /sbin/modprobe ehci_hcd ; /sbin/modprobe -i uhci_hcd ; true

# End /etc/modprobe.d/usb.conf
EOF
#
#		chapter 9.1. The End
#
echo "VMware Photon Linux 1.0 TP2" > %{buildroot}/etc/photon-release
cat > %{buildroot}/etc/lsb-release <<- "EOF"
DISTRIB_ID="VMware Photon"
DISTRIB_RELEASE="1.0 TP2"
DISTRIB_CODENAME=Photon
DISTRIB_DESCRIPTION="VMware Photon 1.0 TP2"
EOF

cat > %{buildroot}/usr/lib/os-release <<- "EOF"
NAME=VMware Photon
VERSION="1.0 TP2"
ID=photon
VERSION_ID=1.0
PRETTY_NAME="VMware Photon/Linux"
ANSI_COLOR="1;34"
HOME_URL="https://vmware.github.io/photon/"
BUG_REPORT_URL="https://github.com/vmware/photon/issues"
EOF

ln -sv ../usr/lib/os-release %{buildroot}/etc/os-release

%files
%defattr(-,root,root)
#	Root filesystem
/bin
%dir /boot
%dir /dev
%dir /etc
%dir /home
/lib

/media
%dir /mnt
/opt
%dir /proc
%dir /root
%dir /run
/sbin
/srv
%dir /sys
%dir /tmp
%dir /usr
%dir /var
#	etc fileystem
%dir /etc/opt
%config(noreplace) /etc/fstab
%config(noreplace) /etc/group
%config(noreplace) /etc/hosts
%config(noreplace) /etc/inputrc
%config(noreplace) /etc/photon-release
%config(noreplace) /etc/lsb-release
%config(noreplace) /usr/lib/os-release
%config(noreplace) /etc/os-release
%config(noreplace) /etc/mtab
%config(noreplace) /etc/passwd
%config(noreplace) /etc/profile
%dir /etc/modprobe.d
%config(noreplace) /etc/modprobe.d/usb.conf
%dir /etc/sysconfig
%config(noreplace) /etc/sysconfig/clock
%config(noreplace) /etc/sysconfig/console
%config(noreplace) /etc/sysconfig/network
%dir /etc/systemd/network
%config(noreplace) /etc/systemd/network/10-dhcp-en.network
%dir /etc/profile.d
#	media filesystem
%dir /run/media/cdrom
%dir /run/media/floppy
#	run filesystem
%dir /run/lock
#	usr filesystem
%dir /mnt/cdrom
%dir /mnt/hgfs
%dir /usr/bin
%dir /usr/include
%dir /usr/lib
%dir /usr/libexec
%dir /usr/local
%dir /usr/local/bin
%dir /usr/local/include
%dir /usr/local/lib
%dir /usr/local/share
%dir /usr/local/share/color
%dir /usr/local/share/dict
%dir /usr/local/share/doc
%dir /usr/local/share/info
%dir /usr/local/share/locale
%dir /usr/local/share/man
%dir /usr/local/share/man/man1
%dir /usr/local/share/man/man2
%dir /usr/local/share/man/man3
%dir /usr/local/share/man/man4
%dir /usr/local/share/man/man5
%dir /usr/local/share/man/man6
%dir /usr/local/share/man/man7
%dir /usr/local/share/man/man8
%dir /usr/local/share/misc
%dir /usr/local/share/terminfo
%dir /usr/local/share/zoneinfo
%dir /usr/local/src
%dir /usr/sbin
%dir /usr/share
%dir /usr/share/color
%dir /usr/share/dict
%dir /usr/share/doc
%dir /usr/share/info
%dir /usr/share/locale
%dir /usr/share/man
%dir /usr/share/man/man1
%dir /usr/share/man/man2
%dir /usr/share/man/man3
%dir /usr/share/man/man4
%dir /usr/share/man/man5
%dir /usr/share/man/man6
%dir /usr/share/man/man7
%dir /usr/share/man/man8
%dir /usr/share/misc
%dir /usr/share/terminfo
%dir /usr/share/zoneinfo
%dir /usr/src
#	var filesystem
%dir /var/cache
%dir /var/lib
%dir /var/lib/color
%dir /var/lib/locate
%dir /var/lib/misc
%dir /var/local
%dir /var/log
%dir /var/mail
%dir /var/mnt
%dir /var/srv
%dir /var/opt
%dir /var/spool
%dir /var/tmp
%attr(-,root,root) 	/var/log/wtmp
%attr(664,root,utmp)	/var/log/lastlog
%attr(600,root,root)	/var/log/btmp
/var/lock
%ghost /var/run
/var/run/lock
#	Symlinks for AMD64
%ifarch x86_64
/lib64
/usr/lib64
/usr/local/lib64
%endif
%changelog
*   Fri Aug 14 2015 Sharath George <sharathg@vmware.com> 7.5-8
-   upgrading release to TP2
*   Tue Jun 30 2015 Alexey Makhalov <amakhalov@vmware.com> 7.5-7
-   /etc/profile.d permission fix
*   Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 7.5-6
-   Adding group dip
*   Mon Jun 22 2015 Divya Thaluru <dthaluru@vmware.com> 7.5-5
-   Fixing lsb-release file
*   Tue Jun 16 2015 Alexey Makhalov <amakhalov@vmware.com> 7.5-4
-   Change users group id to 100.
-   Add audio group to users group.
*   Mon Jun 15 2015 Sharath George <sharathg@vmware.com> 7.5-3
-   Change the network match for dhcp.
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 7.5-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 7.5-1
-   Initial build. First version
