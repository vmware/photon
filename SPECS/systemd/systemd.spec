Summary:          Systemd-228
Name:             systemd
Version:          228
Release:          35%{?dist}
License:          LGPLv2+ and GPLv2+ and MIT
URL:              http://www.freedesktop.org/wiki/Software/systemd/
Group:            System Environment/Security
Vendor:           VMware, Inc.
Distribution:     Photon
Source0:          %{name}-%{version}.tar.gz
%define sha1 systemd=15475d874dc38f8d759f334bbcf7d8aff4b412da
Source1:          99-vmware-hotplug.rules
Source2:          50-security-hardening.conf
#patch for ostree
Patch0:           systemd-228-mount.patch
Patch1:           01-enoX-uses-instance-number-for-vmware-hv.patch
Patch2:           systemd-228-loopback-address.patch
Patch3:           systemd-228-never-cache-localhost-rr.patch
Patch4:           systemd-228-parse-error-message.patch
Patch5:           systemd-228-networking-fixes.patch
Patch6:           systemd-228-cleanup-recv.patch
Patch7:           systemd-228-fix-reading-routes.patch
Patch8:           systemd-228-kernel-ndisc.patch
Patch9:           systemd-228-swap-disconnect-order-fix.patch
Patch10:          systemd-228-duid-iaid-dhcp-preserve.patch
Patch11:          systemd-228-timedatectl-PR2749.patch
Patch12:          systemd-228-query-duid.patch
Patch13:          systemd-228-pam-systemd-user.patch
Patch14:          systemd-228-ipv6-disabled-fix.patch
Patch15:          systemd-228-default-dns-from-env.patch
Patch16:          systemd-228-dhcp-duid-api-update.patch
Patch17:          systemd-228-domains-search-fix.patch
Patch18:          systemd-228-dns-transaction-pending-fix.patch
Patch19:          02-install-general-aliases.patch
Patch20:          systemd-228-CVE-notify-socket-DOS-fix.patch
Patch21:          systemd-macros.patch
Patch22:          systemd-228-vm-watchdog-timer.patch
Patch23:          systemd-228-CVE-2016-10156-suid-fix.patch
Patch24:          systemd-228-CVE-2017-9445-dns-oob.patch
Requires:         Linux-PAM
Requires:         libcap
Requires:         xz
Requires:         kmod
Requires:         glib
BuildRequires:    intltool
BuildRequires:    gperf
BuildRequires:    libcap-devel
BuildRequires:    xz-devel
BuildRequires:    Linux-PAM
BuildRequires:    XML-Parser
BuildRequires:    kbd
BuildRequires:    kmod
BuildRequires:    util-linux-devel
BuildRequires:    libxslt
BuildRequires:    docbook-xsl
BuildRequires:    docbook-xml
BuildRequires:    glib-devel

%description
Systemd is an init replacement with better process control and security

%prep
%setup -q
cat > config.cache << "EOF"
KILL=/bin/kill
HAVE_BLKID=1
BLKID_LIBS="-lblkid"
BLKID_CFLAGS="-I/usr/include/blkid"
cc_cv_CFLAGS__flto=no
EOF
sed -i "s:blkid/::" $(grep -rl "blkid/blkid.h")
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
sed -i "s#\#DefaultTasksMax=512#DefaultTasksMax=infinity#g" src/core/system.conf

%build
./autogen.sh
./configure --prefix=%{_prefix}                                    \
            --sysconfdir=/etc                                       \
            --localstatedir=/var                                    \
            --config-cache                                          \
            --with-rootprefix=                                      \
            --with-rootlibdir=/usr/lib                                  \
            --enable-split-usr                                      \
            --disable-firstboot                                     \
            --disable-ldconfig                                      \
            --disable-sysusers                                      \
            --without-python                                        \
            --enable-pam                                            \
            --docdir=%{_prefix}/share/doc/systemd-228                     \
            --with-dbuspolicydir=/etc/dbus-1/system.d               \
            --with-dbusinterfacedir=%{_prefix}/share/dbus-1/interfaces    \
            --with-dbussessionservicedir=%{_prefix}/share/dbus-1/services \
            --with-dbussystemservicedir=%{_prefix}/share/dbus-1/system-services \
            --enable-compat-libs \
            --with-sysvinit-path=/etc/rc.d/init.d \
            --with-rc-local-script-path-start=/etc/rc.d/rc.local

make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/sbin
for tool in runlevel reboot shutdown poweroff halt telinit; do
     ln -sfv ../bin/systemctl %{buildroot}/sbin/${tool}
done
ln -sfv ../lib/systemd/systemd %{buildroot}/sbin/init
sed -i '/srv/d' %{buildroot}/usr/lib/tmpfiles.d/home.conf
sed -i "s:0775 root lock:0755 root root:g" %{buildroot}/usr/lib/tmpfiles.d/legacy.conf
sed -i "s:NamePolicy=kernel database onboard slot path:NamePolicy=kernel database:g" %{buildroot}/lib/systemd/network/99-default.link
sed -i "s:#LLMNR=yes:LLMNR=false:g" %{buildroot}/etc/systemd/resolved.conf
rm -f %{buildroot}%{_var}/log/README
mkdir -p %{buildroot}%{_localstatedir}/log/journal

#cp %{buildroot}/usr/share/factory/etc/pam.d/system-auth %{buildroot}%{_sysconfdir}/pam.d/system-auth
#cp %{buildroot}/usr/share/factory/etc/pam.d/other %{buildroot}%{_sysconfdir}/pam.d/other
find %{buildroot}%{_libdir} -name '*.la' -delete
install -Dm 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/udev/rules.d
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysctl.d
rm %{buildroot}/lib/systemd/system/default.target
ln -sfv multi-user.target %{buildroot}/lib/systemd/system/default.target

%post
/sbin/ldconfig
%postun
/sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%dir %{_sysconfdir}/systemd
%dir %{_sysconfdir}/systemd/system
%dir %{_sysconfdir}/systemd/user
%dir %{_sysconfdir}/systemd/network
%dir %{_sysconfdir}/tmpfiles.d
%dir %{_sysconfdir}/sysctl.d
%dir %{_sysconfdir}/modules-load.d
%dir %{_sysconfdir}/binfmt.d
%{_sysconfdir}/X11/xinit/xinitrc.d/50-systemd-user.sh
%{_sysconfdir}/sysctl.d/50-security-hardening.conf
%{_sysconfdir}/xdg/systemd
%{_sysconfdir}/rc.d/init.d/README
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.systemd1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.hostname1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.login1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.locale1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.timedate1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.resolve1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.network1.conf
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/org.freedesktop.machine1.conf
%config(noreplace) %{_sysconfdir}/systemd/system.conf
%config(noreplace) %{_sysconfdir}/systemd/user.conf
%config(noreplace) %{_sysconfdir}/systemd/logind.conf
%config(noreplace) %{_sysconfdir}/systemd/journald.conf
%config(noreplace) %{_sysconfdir}/systemd/resolved.conf
%config(noreplace) %{_sysconfdir}/systemd/coredump.conf
%config(noreplace) %{_sysconfdir}/systemd/timesyncd.conf
%config(noreplace) %{_sysconfdir}/systemd/bootchart.conf
%config(noreplace) %{_sysconfdir}/pam.d/systemd-user

%dir %{_sysconfdir}/udev
%dir %{_sysconfdir}/udev/rules.d
%dir %{_sysconfdir}/udev/hwdb.d
%{_sysconfdir}/udev/rules.d/99-vmware-hotplug.rules
%config(noreplace) %{_sysconfdir}/udev/udev.conf
%{_sysconfdir}/systemd/system/*
/lib/udev/*
/lib/systemd/systemd*
/lib/systemd/system-*
/lib/systemd/system/*
/lib/systemd/network/80-container*
%config(noreplace) /lib/systemd/network/99-default.link
%exclude %{_libdir}/debug/*
%{_libdir}/*
%{_bindir}/*
/bin/*
/sbin/*
%{_includedir}/*
%{_datadir}/*
%dir %{_localstatedir}/log/journal

%changelog
*    Thu Jun 29 2017 Vinay Kulkarni <kulkarniv@vmware.com>  228-35
-    Fix for CVE-2017-9445.
*    Sat Jan 22 2017 Vinay Kulkarni <kulkarniv@vmware.com>  228-34
-    Fix for CVE-2016-10156.
*    Sat Jan 21 2017 Vinay Kulkarni <kulkarniv@vmware.com>  228-33
-    Arm watchdog timer more frequently for virtual machine env.
*    Thu Nov 3 2016 Divya Thaluru <dthaluru@vmware.com>  228-32
-    Added logic to reload services incase of rpm upgrade
*    Thu Sep 29 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-31
-    Fix a CVE in systemd-notify socket.
*    Mon Aug 29 2016 Alexey Makhalov <amakhalov@vmware.com>  228-30
-    02-install-general-aliases.patch to create absolute symlinks
*    Fri Aug 26 2016 Anish Swaminathan <anishs@vmware.com>  228-29
-    Change config file properties for 99-default.link
*    Tue Aug 16 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-28
-    systemd-resolved: Fix DNS_TRANSACTION_PENDING assert.
*    Mon Aug 1 2016 Divya Thaluru <dthaluru@vmware.com> 228-27
-    Removed packaging of symlinks and will be created during installation
*    Tue Jul 12 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-26
-    systemd-resolved: Fix DNS domains resolv.conf search issue for static DNS.
*    Mon Jul 11 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-25
-    systemd-networkd: Update DUID/IAID config interface to systemd v230 spec.
*    Tue Jun 21 2016 Anish Swaminathan <anishs@vmware.com>  228-24
-    Change config file properties
*    Fri Jun 17 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-23
-    systemd-resolved: Configure initial DNS servers from environment var.
*    Mon Jun 06 2016 Alexey Makhalov <amakhalov@vmware.com>  228-22
-    systemd-resolved: disable LLMNR
*    Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 228-21
-    GA - Bump release of all rpms
*    Tue May 17 2016 Anish Swaminathan <anishs@vmware.com>  228-20
-    Added patch for letting kernel handle ndisc
*    Tue May 17 2016 Divya Thaluru <dthaluru@vmware.com> 228-19
-    Updated systemd-user PAM configuration
*    Mon May 16 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 228-18
-    Updated the MaxTasks to infinity in system.conf file
*    Thu Apr 21 2016 Mahmoud Bassiouny <mbassiouny@vmware.com>  228-17
-    Set the default.target to the multi-user.target
*    Tue Apr 12 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-16
-    Disable network interface renaming.
*    Thu Mar 31 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-15
-    Patch to query DHCP DUID, IAID.f
*    Wed Mar 30 2016 Vinay Kulkarni <kulkarniv@vmware.com>  228-14
-    Update DHCP DUID, IAID configuration patch.
*    Wed Mar 30 2016 Kumar Kaushik <kaushikk@vmware.com>  228-13
-    Install the security hardening script as part of systemd.
*    Tue Mar 29 2016 Kumar Kaushik <kaushikk@vmware.com>  228-12
-    Added patch for timedatectl /etc/adjtime PR2749.
*    Fri Mar 11 2016 Anish Swaminathan <anishs@vmware.com>  228-11
-    Added patch for dhcp preservation via duid iaid configurability
*    Fri Mar 11 2016 Anish Swaminathan <anishs@vmware.com>  228-10
-    Added patch for swap disconnect order
*    Thu Mar 10 2016 XIaolin Li <xiaolinl@vmware.com> 228-9
-    Enable manpages.
*    Fri Feb 19 2016 Anish Swaminathan <anishs@vmware.com>  228-8
-    Added patch to get around systemd-networkd wait online timeout
*    Sat Feb 06 2016 Alexey Makhalov <amakhalov@vmware.com>  228-7
-    Added patch: fix-reading-routes.
*    Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com>  228-6
-    Add hotplug udev rules.
*    Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  228-5
-    Change config file attributes.
*    Wed Jan 06 2016 Anish Swaminathan <anishs@vmware.com> 228-4
-    Patches for minor network fixes.
*    Wed Dec 16 2015 Anish Swaminathan <anishs@vmware.com> 228-3
-    Patch for ostree.
*    Wed Dec 16 2015 Anish Swaminathan <anishs@vmware.com> 228-2
-    Patch for loopback address.
*    Fri Dec 11 2015 Anish Swaminathan <anishs@vmware.com> 228-1
-    Upgrade systemd version.
*    Mon Nov 30 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 216-13
-    Removing the reference of lock user
*    Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 216-12
-    Removing la files from packages.
*    Fri Sep 18 2015 Divya Thaluru <dthaluru@vmware.com> 216-11
-    Packaging journal log directory
*    Thu Sep 10 2015 Alexey Makhalov <amakhalov@vmware.com> 216-10
-    Improve enoX renaming in VMware HV case. Patch is added.
*    Tue Aug 25 2015 Alexey Makhalov <amakhalov@vmware.com> 216-9
-    Reduce systemd-networkd boot time (exclude if-rename patch).
*    Mon Jul 20 2015 Divya Thaluru <dthaluru@vmware.com> 216-8
-    Adding sysvinit support 
*    Mon Jul 06 2015 Kumar Kaushik <kaushikk@vmware.com> 216-7
-    Fixing networkd/udev race condition for renaming interface.
*    Thu Jun 25 2015 Sharath George <sharathg@vmware.com> 216-6
-    Remove debug files.
*    Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 216-5
-    Building compat libs 
*    Mon Jun 1 2015 Alexey Makhalov <amakhalov@vmware.com> 216-4
-    gudev support
*    Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> 216-3
-    Removing packing of PAM configuration files
*    Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 216-2
-    Update according to UsrMove.
*    Mon Oct 27 2014 Sharath George <sharathg@vmware.com> 216-1
-    Initial build. First version
