Summary:        Cyrus Simple Authentication Service Layer (SASL) library
Name:           cyrus-sasl
Version:        2.1.26
Release:        15%{?dist}
License:        Custom
URL:            http://cyrusimap.web.cmu.edu/
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        ftp://ftp.cyrusimap.org/cyrus-sasl/%{name}-%{version}.tar.gz
%define sha1    cyrus-sasl=d6669fb91434192529bd13ee95737a8a5040241c
Patch0:         http://www.linuxfromscratch.org/patches/blfs/svn/cyrus-sasl-2.1.26-fixes-3.patch
Patch1:         cyrus-sasl-mem-leak-fix.patch
Patch2:         cyrus-sasl-2.1.26-fix-cross-compiling.patch
Patch3:         cyrus-sasl-2.1.26-fix-cross-compiling-again.patch
BuildRequires:  systemd
BuildRequires:  openssl-devel
BuildRequires:  krb5-devel >= 1.12
BuildRequires:  e2fsprogs-devel
BuildRequires:  Linux-PAM-devel
Requires:       openssl
Requires:       krb5 >= 1.12
Requires:       Linux-PAM
Requires:       systemd
%description
The Cyrus SASL package contains a Simple Authentication and Security 
Layer, a method for adding authentication support to 
connection-based protocols. To use SASL, a protocol includes a command
for identifying and authenticating a user to a server and for 
optionally negotiating protection of subsequent protocol interactions.
If its use is negotiated, a security layer is inserted between the 
protocol and the connection.
%prep
%setup -q
%patch0 -p1
%patch1 -p1
if [ %{_host} != %{_build} ]; then
%patch2 -p1
%patch3 -p1
fi
%build
autoreconf -fi
pushd saslauthd
autoreconf -fi
popd
%configure \
    CFLAGS="%{optflags} -fPIC" \
    CXXFLAGS="%{optflags}" \
    --with-plugindir=%{_libdir}/sasl2 \
    --without-dblib \
    --with-saslauthd=/run/saslauthd \
    --without-authdaemond \
    --disable-macos-framework \
    --disable-sample \
    --disable-digest \
    --disable-otp \
    --disable-plain \
    --disable-anon \
    --enable-srp \
    --enable-gss_mutexes \
    --disable-static \
    --enable-shared \
    --enable-fast-install \
    --enable-krb4

make
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.la' -delete
install -D -m644 COPYING %{buildroot}/usr/share/licenses/%{name}/LICENSE
%{_fixperms} %{buildroot}/*

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat << EOF >> %{buildroot}/%{_sysconfdir}/sysconfig/saslauthd
# Directory in which to place saslauthd's listening socket, pid file, and so
# on.  This directory must already exist.
SOCKETDIR=/run/saslauthd

# Mechanism to use when checking passwords.  Run "saslauthd -v" to get a list
# of which mechanism your installation was compiled with the ablity to use.
MECH=pam

# Additional flags to pass to saslauthd on the command line.  See saslauthd(8)
# for the list of accepted flags.
FLAGS=
EOF

mkdir -p %{buildroot}/lib/systemd/system
cat << EOF >> %{buildroot}/lib/systemd/system/saslauthd.service
[Unit]
Description=SASL authentication daemon.

[Service]
Type=forking
PIDFile=/run/saslauthd/saslauthd.pid
EnvironmentFile=/etc/sysconfig/saslauthd
ExecStart=/usr/sbin/saslauthd -m \$SOCKETDIR -a \$MECH \$FLAGS
RuntimeDirectory=saslauthd

[Install]
WantedBy=multi-user.target
EOF

install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable saslauthd.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-saslauthd.preset

%check
make %{?_smp_mflags} check

%post
%{_sbindir}/ldconfig 
%systemd_post saslauthd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart saslauthd.service

%preun
%systemd_preun saslauthd.service

%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/etc/sysconfig/saslauthd
/lib/systemd/system/saslauthd.service
%{_libdir}/systemd/system-preset/50-saslauthd.preset
%{_includedir}/*
%{_libdir}/*.so*
%{_libdir}/pkgconfig/*
%{_libdir}/sasl2/*
%{_sbindir}/*
%{_mandir}/man3/*
%{_datadir}/licenses/%{name}/LICENSE
%{_mandir}/man8/saslauthd.8.gz

%changelog
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 2.1.26-15
-   Cross compilation support
*   Tue Nov 21 2017 Anish Swaminathan <anishs@vmware.com>  2.1.26-14
-   Update patch for memory leak fix
*   Tue Oct 10 2017 Anish Swaminathan <anishs@vmware.com>  2.1.26-13
-   Add patch for memory leak fix
*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  2.1.26-12
-   Disabled saslauthd service by default
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.1.26-11
-   BuildRequires Linux-PAM-devel
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2.1.26-10
-   Required krb5-devel.
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.1.26-9
-   Modified %check
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2.1.26-8
-   Fixed logic to restart the active services after upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.26-7
-   GA - Bump release of all rpms
*   Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  2.1.26-6
-   Fixing spec file to handle rpm upgrade scenario correctly
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  2.1.26-5
-   Add systemd to Requires and BuildRequires.
*   Wed Nov 11 2015 Xiaolin Li <xiaolinl@vmware.com> 2.1.26-4
-   Add saslauthd service to systemd.
*   Tue Sep 01 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.1.26-3
-   Enable CRAM.
*   Thu Jul 16 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.26-2
-   Disabling parallel threads in make
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.1.26-1
-   Initial build. First version
