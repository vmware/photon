Summary:    Default file system
Name:       filesystem
Version:    1.1
Release:    5%{?dist}
License:    GPLv3
Group:      System Environment/Base
Vendor:     VMware, Inc.
URL:        http://www.linuxfromscratch.org
Distribution:   Photon

Source0: clock
Source1: console
Source2: hosts
Source3: inputrc
Source4: profile
Source5: proxy
Source6: proxy.sh
Source7: usb.conf
Source8: group
Source9: passwd

%description
The filesystem package is one of the basic packages that is installed
on a Linux system. Filesystem contains the basic directory
layout for a Linux operating system, including the correct permissions
for the directories. This version is for a system configured with systemd.

%prep
%build

%install
install -vdm 755 %{buildroot}/{dev,proc,run/{media/{floppy,cdrom},lock},sys}
install -vdm 755 %{buildroot}/{boot,etc/{opt,sysconfig},home,mnt}
install -vdm 755 %{buildroot}/{var}
install -dv -m 0750 %{buildroot}/root
install -dv -m 1777 %{buildroot}/tmp %{buildroot}%{_var}/tmp
install -vdm 755 %{buildroot}%{_usr}/{,local/}{bin,include,lib,sbin,src}
install -vdm 755 %{buildroot}%{_usr}/{,local/}share/{color,dict,doc,info,locale,man}
install -vdm 755 %{buildroot}%{_usr}/{,local/}share/{misc,terminfo,zoneinfo}
install -vdm 755 %{buildroot}%{_libexecdir}
install -vdm 755 %{buildroot}%{_usr}/{,local/}share/man/man{1..8}
install -vdm 755 %{buildroot}%{_sysconfdir}/profile.d
install -vdm 755 %{buildroot}%{_libdir}/debug/{lib,bin,sbin,usr}

ln -svfn usr/lib %{buildroot}/lib
ln -svfn usr/bin %{buildroot}/bin
ln -svfn usr/sbin %{buildroot}/sbin
ln -svfn run/media %{buildroot}/media

ln -svfn ../bin %{buildroot}%{_libdir}/debug%{_bindir}
ln -svfn ../sbin %{buildroot}%{_libdir}/debug%{_sbindir}
ln -svfn ../lib %{buildroot}%{_libdir}/debug%{_libdir}

ln -svfn usr/lib %{buildroot}/lib64
ln -svfn lib %{buildroot}%{_lib64dir}
ln -svfn lib %{buildroot}%{_usr}/local/lib64
ln -svfn lib %{buildroot}%{_libdir}/debug/lib64
ln -svfn ../lib %{buildroot}%{_libdir}/debug%{_lib64dir}

install -vdm 755 %{buildroot}%{_var}/{log,mail,spool,mnt,srv}

ln -svfn var/srv %{buildroot}/srv
ln -svfn ../run %{buildroot}%{_var}/run
ln -svfn ../run/lock %{buildroot}%{_var}/lock
install -vdm 755 %{buildroot}%{_var}/{opt,cache,lib/{color,misc,locate},local}
install -vdm 755 %{buildroot}/mnt/cdrom
install -vdm 755 %{buildroot}/mnt/hgfs

#   6.6. Creating Essential Files and Symlinks
ln -svfn /proc/self/mounts %{buildroot}%{_sysconfdir}/mtab

touch %{buildroot}%{_var}/log/{btmp,wtmp}

# Configuration files
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/group
install -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/passwd

# Creating Proxy Configuration
install -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/proxy

#   7.3. Customizing the /etc/hosts File
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/hosts

#   7.9. Configuring the setclock Script"
install -m 644 %{SOURCE0} %{buildroot}%{_sysconfdir}/sysconfig/clock

#   7.10. Configuring the Linux Console"
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/console

#   7.13. The Bash Shell Startup Files
install -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/profile

#   The Proxy Bash Shell Startup File
install -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/profile.d/proxy.sh

#   7.14. Creating the /etc/inputrc File
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/inputrc

#   8.2. Creating the /etc/fstab File
touch %{buildroot}%{_sysconfdir}/fstab

#   8.3.2. Configuring Linux Module Load Order
install -vdm 755 %{buildroot}%{_sysconfdir}/modprobe.d
install -m 644 %{SOURCE7} %{buildroot}%{_sysconfdir}/modprobe.d/usb.conf
#       chapter 9.1. The End

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
#   Root filesystem
/bin
%dir /boot
%dir /dev
%dir %{_sysconfdir}
%dir /home
/lib

/media
%dir /mnt
%dir /proc
%dir /root
%dir /run
/sbin
/srv
%dir /sys
%dir /tmp
%dir %{_usr}
%dir %{_var}
#   etc fileystem
%dir %{_sysconfdir}/opt
%config(noreplace) %{_sysconfdir}/fstab
%config(noreplace) %{_sysconfdir}/group
%config(noreplace) %{_sysconfdir}/hosts
%config(noreplace) %{_sysconfdir}/inputrc
%config(noreplace) %{_sysconfdir}/mtab
%config(noreplace) %{_sysconfdir}/passwd
%config(noreplace) %{_sysconfdir}/profile
%dir %{_sysconfdir}/modprobe.d
%config(noreplace) %{_sysconfdir}/modprobe.d/usb.conf
%dir %{_sysconfdir}/sysconfig
%config(noreplace) %{_sysconfdir}/sysconfig/clock
%config(noreplace) %{_sysconfdir}/sysconfig/console
%config(noreplace) %{_sysconfdir}/sysconfig/proxy
%dir %{_sysconfdir}/profile.d
%config(noreplace) %{_sysconfdir}/profile.d/proxy.sh
#   media filesystem
%dir /run/media/cdrom
%dir /run/media/floppy
#   run filesystem
%dir /run/lock
#   usr filesystem
%dir /mnt/cdrom
%dir /mnt/hgfs
%dir %{_bindir}
%dir %{_includedir}
%dir %{_libdir}
%dir %{_libdir}/debug
%dir %{_libdir}/debug/bin
%dir %{_libdir}/debug/lib
%dir %{_libdir}/debug/sbin
%{_libdir}/debug%{_bindir}
%{_libdir}/debug%{_libdir}
%{_libdir}/debug%{_sbindir}
%dir %{_libexecdir}
%dir %{_usr}/local
%dir %{_usr}/local/bin
%dir %{_usr}/local/include
%dir %{_usr}/local/lib
%dir %{_usr}/local/share
%dir %{_usr}/local/share/color
%dir %{_usr}/local/share/dict
%dir %{_usr}/local/share/doc
%dir %{_usr}/local/share/info
%dir %{_usr}/local/share/locale
%dir %{_usr}/local/share/man
%dir %{_usr}/local/share/man/man1
%dir %{_usr}/local/share/man/man2
%dir %{_usr}/local/share/man/man3
%dir %{_usr}/local/share/man/man4
%dir %{_usr}/local/share/man/man5
%dir %{_usr}/local/share/man/man6
%dir %{_usr}/local/share/man/man7
%dir %{_usr}/local/share/man/man8
%dir %{_usr}/local/share/misc
%dir %{_usr}/local/share/terminfo
%dir %{_usr}/local/share/zoneinfo
%dir %{_usr}/local/src
%dir %{_sbindir}
%dir %{_datadir}
%dir %{_datadir}/color
%dir %{_datadir}/dict
%dir %{_datadir}/doc
%dir %{_datadir}/info
%dir %{_datadir}/locale
%dir %{_mandir}
%dir %{_mandir}/man1
%dir %{_mandir}/man2
%dir %{_mandir}/man3
%dir %{_mandir}/man4
%dir %{_mandir}/man5
%dir %{_mandir}/man6
%dir %{_mandir}/man7
%dir %{_mandir}/man8
%dir %{_datadir}/misc
%dir %{_datadir}/terminfo
%dir %{_datadir}/zoneinfo
%dir %{_usrsrc}
#   var filesystem
%dir %{_var}/cache
%dir %{_sharedstatedir}
%dir %{_sharedstatedir}/color
%dir %{_sharedstatedir}/locate
%dir %{_sharedstatedir}/misc
%dir %{_var}/local
%dir %{_var}/log
%dir %{_var}/mail
%dir %{_var}/mnt
%dir %{_var}/srv
%dir %{_var}/opt
%dir %{_var}/spool
%dir %{_var}/tmp
%attr(-,root,root)  %{_var}/log/wtmp
%attr(600,root,root) %{_var}/log/btmp
%{_var}/lock
%{_var}/run

/lib64
%{_lib64dir}
%{_usr}/local/lib64
%{_libdir}/debug/lib64
%{_libdir}/debug%{_lib64dir}

%changelog
* Tue Aug 27 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1-5
- Keep static data in files
- Remove lastlog file and utmp group
* Wed Sep 23 2020 Michelle Wang <michellew@vmware.com> 1.1-4
- Add sources0 for OSSTP tickets
* Wed May 8 2019 Alexey Makhalov <amakhalov@vmware.com> 1.1-3
- Set 'x' as a root password placeholder
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.1-2
- Aarch64 support
* Fri Sep 15 2017 Anish Swaminathan <anishs@vmware.com>  1.1-1
- Move network file from filesystem package
* Fri Apr 21 2017 Alexey Makhalov <amakhalov@vmware.com> 1.0-13
- make /var/run symlink to /run and keep it in rpm
* Thu Apr 20 2017 Bo Gan <ganb@vmware.com> 1.0-12
- Fix /usr/local/lib64 symlink
* Wed Mar 08 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.0-11
- Create default DHCP net config in 99-dhcp-en.network instead of 10-dhcp-en.network
* Wed Aug 24 2016 Alexey Makhalov <amakhalov@vmware.com> 1.0-10
- /etc/inputrc PgUp/PgDown for history search
* Tue Jul 12 2016 Divya Thaluru <dthaluru@vmware.com> 1.0-9
- Added filesystem for debug libraries and binaries
* Fri Jul 8 2016 Divya Thaluru <dthaluru@vmware.com> 1.0-8
- Removing multiple entries of localhost in /etc/hosts file
* Fri May 27 2016 Divya Thaluru <dthaluru@vmware.com> 1.0-7
- Fixed nobody user uid and group gid
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0-6
- GA - Bump release of all rpms
* Wed May 4 2016 Divya Thaluru <dthaluru@vmware.com> 1.0-5
- Removing non-existent users from /etc/group file
* Fri Apr 29 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 1.0-4
- Updating the /etc/hosts file
* Fri Apr 22 2016 Divya Thaluru <dthaluru@vmware.com> 1.0-3
- Setting default umask value to 027
* Thu Apr 21 2016 Anish Swaminathan <anishs@vmware.com> 1.0-2
- Version update for network file change
* Mon Jan 18 2016 Anish Swaminathan <anishs@vmware.com> 1.0-1
- Reset version to match with Photon version
* Wed Jan 13 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 7.5-13
- Support to set proxy configuration file - SLES proxy configuration implementation.
* Thu Jan 7 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 7.5-12
- Removing /etc/sysconfig/network file.
* Mon Nov 16 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 7.5-11
- Removing /etc/fstab mount entries.
* Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 7.5-10
- Removint /opt from filesystem.
* Fri Oct 02 2015 Vinay Kulkarni <kulkarniv@vmware.com> 7.5-9
- Dump build-number and release version from macros.
* Fri Aug 14 2015 Sharath George <sharathg@vmware.com> 7.5-8
- upgrading release to TP2
* Tue Jun 30 2015 Alexey Makhalov <amakhalov@vmware.com> 7.5-7
- /etc/profile.d permission fix
* Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 7.5-6
- Adding group dip
* Mon Jun 22 2015 Divya Thaluru <dthaluru@vmware.com> 7.5-5
- Fixing lsb-release file
* Tue Jun 16 2015 Alexey Makhalov <amakhalov@vmware.com> 7.5-4
- Change users group id to 100.
- Add audio group to users group.
* Mon Jun 15 2015 Sharath George <sharathg@vmware.com> 7.5-3
- Change the network match for dhcp.
* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 7.5-2
- Update according to UsrMove.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 7.5-1
- Initial build. First version
