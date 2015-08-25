Summary:	Systemd-216
Name:		systemd
Version:	216
Release:	9%{?dist}
License:	LGPLv2+ and GPLv2+ and MIT
URL:		http://www.freedesktop.org/wiki/Software/systemd/
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.freedesktop.org/software/systemd/%{name}-%{version}.tar.xz
%define sha1 systemd=0d933a2f76db5d30f52429e9b172323bc6abd49a
Patch0:     	systemd-216-compat-1.patch
Requires:	Linux-PAM
Requires:	libcap
Requires:	xz
BuildRequires:	intltool
BuildRequires:	gperf
BuildRequires:	libcap
BuildRequires:	xz-devel
BuildRequires:	Linux-PAM
BuildRequires:	XML-Parser
BuildRequires:	kbd
BuildRequires:	kmod
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
%build
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
            --docdir=%{_prefix}/share/doc/systemd-216                     \
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
rm -f %{buildroot}%{_var}/log/README

#cp %{buildroot}/usr/share/factory/etc/pam.d/system-auth %{buildroot}%{_sysconfdir}/pam.d/system-auth
#cp %{buildroot}/usr/share/factory/etc/pam.d/other %{buildroot}%{_sysconfdir}/pam.d/other

%post	-p /sbin/ldconfig
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


%changelog
*	Tue Aug 25 2015 Alexey Makhalov <amakhalov@vmware.com> 216-9
-	Reduce systemd-networkd boot time (exclude if-rename patch).
*	Tue Jul 20 2015 Divya Thaluru <dthaluru@vmware.com> 216-8
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
