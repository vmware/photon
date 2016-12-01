Summary:          Systemd-232
Name:             systemd
Version:          232
Release:          2%{?dist}
License:          LGPLv2+ and GPLv2+ and MIT
URL:              http://www.freedesktop.org/wiki/Software/systemd/
Group:            System Environment/Security
Vendor:           VMware, Inc.
Distribution:     Photon
Source0:          %{name}-%{version}.tar.gz
%define sha1 systemd=74178b96d631058236cf79f5b0cc3953382f12b5
Source1:          99-vmware-hotplug.rules
Source2:          50-security-hardening.conf

Patch0:           01-enoX-uses-instance-number-for-vmware-hv.patch
Patch1:           02-install-general-aliases.patch
Patch2:           systemd-232-query-duid.patch
Patch3:           systemd-232-ipv6-disabled-fix.patch
Patch4:           systemd-232-default-dns-from-env.patch
Patch5:           systemd-macros.patch
Patch6:           systemd-232-resolv-conf-symlink.patch

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

%package devel
Summary:        Development headers for systemd
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers for developing applications linking to libsystemd

%package lang
Summary:        Language pack for systemd
Requires:       %{name} = %{version}-%{release}

%description lang
Language pack for systemd

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
            --disable-elfutils \
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
find %{buildroot} -name '*.la' -delete
install -Dm 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/udev/rules.d
install -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysctl.d
rm %{buildroot}/lib/systemd/system/default.target
ln -sfv multi-user.target %{buildroot}/lib/systemd/system/default.target
%find_lang %{name}

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
/lib/systemd/*.so
/lib/systemd/resolv.conf
%config(noreplace) /lib/systemd/network/99-default.link
%exclude %{_libdir}/debug
%exclude %{_datadir}/locale
%{_libdir}/binfmt.d
%{_libdir}/kernel
%{_libdir}/modules-load.d
%{_libdir}/rpm
%{_libdir}/security
%{_libdir}/sysctl.d
%{_libdir}/systemd
%{_libdir}/tmpfiles.d
%{_libdir}/*.so*
%{_bindir}/*
/bin/*
/sbin/*
%{_datadir}/bash-completion/*
%{_datadir}/factory/*
%{_datadir}/dbus-1
%{_datadir}/doc/*
%{_mandir}/*
%{_datadir}/polkit-1
%{_datadir}/systemd
%{_datadir}/zsh/*
%dir %{_localstatedir}/log/journal

%files devel
%dir %{_includedir}/systemd
%{_libdir}/libudev.so
%{_libdir}/libsystemd.so
%{_includedir}/systemd/*.h
%{_includedir}/libudev.h
%{_libdir}/pkgconfig/libudev.pc
%{_libdir}/pkgconfig/libsystemd.pc
%{_datadir}/pkgconfig/systemd.pc
%{_datadir}/pkgconfig/udev.pc

%files lang -f %{name}.lang

%changelog
*    Thu Dec 01 2016 Xiaolin Li <xiaolinl@vmware.com> 232-2
-    disable-elfutils.
*    Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  232-1
-    Update systemd to 232
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
