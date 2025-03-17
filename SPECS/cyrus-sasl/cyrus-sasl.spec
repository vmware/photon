%define socket_dir  /run/saslauthd

Summary:        Cyrus Simple Authentication Service Layer (SASL) library
Name:           cyrus-sasl
Version:        2.1.28
Release:        5%{?dist}
URL:            https://github.com/cyrusimap/cyrus-sasl
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/cyrusimap/cyrus-sasl/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  systemd-devel
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

%package devel
Requires: %{name} = %{version}-%{release}
Requires: pkg-config
Summary: Files needed for developing applications with Cyrus SASL

%description devel
The %{name}-devel package contains files needed for developing and
compiling applications which use the Cyrus SASL library.

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

%build
sh ./autogen.sh
%configure \
    CFLAGS="%{optflags} -fPIC" \
    CXXFLAGS="%{optflags}" \
    --with-plugindir=%{_libdir}/sasl2 \
    --without-dblib \
    --with-saslauthd=%{socket_dir} \
    --without-authdaemond \
    --disable-macos-framework \
    --disable-sample \
    --disable-digest \
    --disable-otp \
    --enable-plain \
    --enable-login \
    --disable-anon \
    --enable-srp \
    --enable-gss_mutexes \
    --disable-static \
    --enable-shared \
    --enable-fast-install \
    --enable-krb4

%make_build

%install
%make_install %{?_smp_mflags}
%{_fixperms} %{buildroot}/*

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat << EOF >> %{buildroot}%{_sysconfdir}/sysconfig/saslauthd
# Directory in which to place saslauthd's listening socket, pid file, and so
# on.  This directory must already exist.
SOCKETDIR=%{socket_dir}

# Mechanism to use when checking passwords.  Run "saslauthd -v" to get a list
# of which mechanism your installation was compiled with the ablity to use.
MECH=pam

# Additional flags to pass to saslauthd on the command line.  See saslauthd(8)
# for the list of accepted flags.
FLAGS=
EOF

mkdir -p %{buildroot}%{_unitdir}
cat << EOF >> %{buildroot}%{_unitdir}/saslauthd.service
[Unit]
Description=SASL authentication daemon.

[Service]
Type=forking
PIDFile=%{socket_dir}/saslauthd.pid
EnvironmentFile=%{_sysconfdir}/sysconfig/saslauthd
ExecStart=%{_sbindir}/saslauthd -m \$SOCKETDIR -a \$MECH \$FLAGS
RuntimeDirectory=saslauthd

[Install]
WantedBy=multi-user.target
EOF

install -vdm755 %{buildroot}%{_presetdir}
echo "disable saslauthd.service" > %{buildroot}%{_presetdir}/50-saslauthd.preset

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post
/sbin/ldconfig
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
%{_sysconfdir}/sysconfig/saslauthd
%{_unitdir}/saslauthd.service
%{_presetdir}/50-saslauthd.preset
%{_libdir}/*.so.*
%{_libdir}/sasl2/*.so.*
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/sasl2/*.so
%{_mandir}/man3/*
%{_mandir}/man8/saslauthd.8.gz
%{_mandir}/man8/testsaslauthd.8.gz
%{_libdir}/pkgconfig/*
%{_includedir}/*

%changelog
* Wed Dec 11 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 2.1.28-5
- Release bump for SRP compliance
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 2.1.28-4
- Bump version as a part of krb5 upgrade
* Tue Feb 07 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.1.28-3
- Add devel sub package
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.1.28-2
- Bump version as a part of krb5 upgrade
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.1.28-1
- Automatic Version Bump
* Fri Mar 04 2022 Nitesh Kumar <kunitesh@vmware.com> 2.1.27-6
- Fix CVE-2022-24407
* Thu Sep 02 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.1.27-5
- Bump up release for openssl
* Fri Oct 30 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com>  2.1.27-4
- Fix CVE-2019-19906
* Mon Oct 05 2020 Tapas Kundu <tkundu@vmware.com> 2.1.27-3
- Enable login and plain
* Tue Sep 01 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com>  2.1.27-2
- Make openssl 1.1.1 compatible
* Mon Aug 17 2020 Gerrit Photon <photon-checkins@vmware.com> 2.1.27-1
- Automatic Version Bump
* Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 2.1.26-15
- Cross compilation support
* Tue Nov 21 2017 Anish Swaminathan <anishs@vmware.com>  2.1.26-14
- Update patch for memory leak fix
* Tue Oct 10 2017 Anish Swaminathan <anishs@vmware.com>  2.1.26-13
- Add patch for memory leak fix
* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  2.1.26-12
- Disabled saslauthd service by default
* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.1.26-11
- BuildRequires Linux-PAM-devel
* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2.1.26-10
- Required krb5-devel.
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.1.26-9
- Modified %check
* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2.1.26-8
- Fixed logic to restart the active services after upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.26-7
- GA - Bump release of all rpms
* Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  2.1.26-6
- Fixing spec file to handle rpm upgrade scenario correctly
* Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  2.1.26-5
- Add systemd to Requires and BuildRequires.
* Wed Nov 11 2015 Xiaolin Li <xiaolinl@vmware.com> 2.1.26-4
- Add saslauthd service to systemd.
* Tue Sep 01 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.1.26-3
- Enable CRAM.
* Thu Jul 16 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.26-2
- Disabling parallel threads in make
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.1.26-1
- Initial build. First version.
