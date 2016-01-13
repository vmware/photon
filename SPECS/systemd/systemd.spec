Summary:	Systemd-228
Name:		systemd
Version:	228
Release:	5%{?dist}
License:	LGPLv2+ and GPLv2+ and MIT
URL:		http://www.freedesktop.org/wiki/Software/systemd/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	%{name}-%{version}.tar.gz
%define sha1 systemd=15475d874dc38f8d759f334bbcf7d8aff4b412da
#patch for ostree
Patch0:         systemd-228-mount.patch
Patch1:         01-enoX-uses-instance-number-for-vmware-hv.patch
Patch2:         systemd-228-loopback-address.patch
Patch3:         systemd-228-never-cache-localhost-rr.patch
Patch4:         systemd-228-parse-error-message.patch
Patch5:         systemd-228-networking-fixes.patch
Patch6:         systemd-228-cleanup-recv.patch
Requires:	Linux-PAM
Requires:	libcap
Requires:	xz
BuildRequires:	intltool
BuildRequires:	gperf
BuildRequires:	libcap-devel
BuildRequires:	xz-devel
BuildRequires:	Linux-PAM
BuildRequires:	XML-Parser
BuildRequires:	kbd
BuildRequires:	kmod
BuildRequires:	util-linux-devel
Requires:	kmod
BuildRequires:	glib-devel
Requires:	glib
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
            --disable-manpages                                      \
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
sed -i "s:0775 root lock:0755 root root:g" %{buildroot}/usr/lib/tmpfiles.d/legacy.conf
rm -f %{buildroot}%{_var}/log/README
mkdir -p %{buildroot}%{_localstatedir}/log/journal

#cp %{buildroot}/usr/share/factory/etc/pam.d/system-auth %{buildroot}%{_sysconfdir}/pam.d/system-auth
#cp %{buildroot}/usr/share/factory/etc/pam.d/other %{buildroot}%{_sysconfdir}/pam.d/other
find %{buildroot}%{_libdir} -name '*.la' -delete
%post
/sbin/ldconfig
%postun	
/sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_sysconfdir}/*
/lib/*
%exclude %{_libdir}/debug/*
%{_libdir}/*
%{_bindir}/*
/bin/*
/sbin/*
%{_includedir}/*
%{_datadir}/*
%dir %{_localstatedir}/log/journal


%changelog
*       Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  228-5
-       Change config file attributes.
*       Wed Jan 06 2016 Anish Swaminathan <anishs@vmware.com> 228-4
-       Patches for minor network fixes.
*       Wed Dec 16 2015 Anish Swaminathan <anishs@vmware.com> 228-3
-       Patch for ostree.
*   	Wed Dec 16 2015 Anish Swaminathan <anishs@vmware.com> 228-2
-   	Patch for loopback address.
*   	Fri Dec 11 2015 Anish Swaminathan <anishs@vmware.com> 228-1
-   	Upgrade systemd version.
*     	Mon Nov 30 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 216-13
-    	Removing the reference of lock user
*     	Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 216-12
-     	Removing la files from packages.
*	Fri Sep 18 2015 Divya Thaluru <dthaluru@vmware.com> 216-11
-	Packaging journal log directory
*	Thu Sep 10 2015 Alexey Makhalov <amakhalov@vmware.com> 216-10
-	Improve enoX renaming in VMware HV case. Patch is added.
*	Tue Aug 25 2015 Alexey Makhalov <amakhalov@vmware.com> 216-9
-	Reduce systemd-networkd boot time (exclude if-rename patch).
*	Mon Jul 20 2015 Divya Thaluru <dthaluru@vmware.com> 216-8
-	Adding sysvinit support 
*       Mon Jul 06 2015 Kumar Kaushik <kaushikk@vmware.com> 216-7
-       Fixing networkd/udev race condition for renaming interface.
*   	Thu Jun 25 2015 Sharath George <sharathg@vmware.com> 216-6
-   	Remove debug files.
*	Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 216-5
-	Building compat libs 
*	Mon Jun 1 2015 Alexey Makhalov <amakhalov@vmware.com> 216-4
-	gudev support
*	Wed May 27 2015 Divya Thaluru <dthaluru@vmware.com> 216-3
-	Removing packing of PAM configuration files
*   	Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 216-2
-   	Update according to UsrMove.
*	Mon Oct 27 2014 Sharath George <sharathg@vmware.com> 216-1
-	Initial build.	First version
