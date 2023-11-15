Summary:        TPM2 Access Broker & Resource Management Daemon implementing the TCG spec
Name:           tpm2-abrmd
Version:        2.4.1
Release:        2%{?dist}
License:        BSD 2-Clause
URL:            https://github.com/tpm2-software/tpm2-abrmd
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/tpm2-software/tpm2-abrmd/releases/download/2.4.1/%{name}-%{version}.tar.gz
%define sha512  tpm2=0335285678cfceca4f185981ded90d213ff796cadddc9b5d6dbf2db533f81023a0f1089bbd8a8017bccb95190889be23b24d38a176d3368d221479aff4ff7d6c

BuildRequires:  which
BuildRequires:  dbus-devel
BuildRequires:  glib-devel >= 2.58.3
BuildRequires:  tpm2-tss-devel
BuildRequires:  systemd-devel

Requires: systemd
Requires: dbus
Requires: glib >= 2.58.3
Requires: tpm2-tss

%description
TPM2 Access Broker & Resource Management Daemon implementing the TCG spec

%package        devel
Summary:        The libraries and header files needed for TSS2 ABRMD development.
Requires:       %{name} = %{version}-%{release}

%description    devel
The libraries and header files needed for TSS2 ABRMD development.

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --with-systemdsystemunitdir=%{_unitdir} \
    --with-dbuspolicydir=%{_sysconfdir}/dbus-1/system.d

%make_build

%install
%make_install %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/dbus-1/system.d/%{name}.conf
%{_sbindir}/%{name}
%{_libdir}/libtss2-tcti-tabrmd.so.0
%{_libdir}/libtss2-tcti-tabrmd.so.0.0.0
%{_unitdir}/%{name}.service
%{_prefix}%{_presetdir}/%{name}.preset
%{_datadir}/dbus-1/*
%{_mandir}/man8

%files devel
%defattr(-,root,root)
%{_includedir}/tss2/*
%{_libdir}/pkgconfig/*
%{_libdir}/libtss2-tcti-tabrmd.so
%{_mandir}/man3
%{_mandir}/man7

%changelog
* Wed Nov 15 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com>  2.4.1-2
- Version bump due to glib change
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.4.1-1
- Remove .la files
* Mon Dec 14 2020 Gerrit Photon <photon-checkins@vmware.com> 2.1.1-1
- Automatic Version Bump
* Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.1.0-1
- Initial build. First version
