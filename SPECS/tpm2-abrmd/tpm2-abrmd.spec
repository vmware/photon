Summary:        TPM2 Access Broker & Resource Management Daemon implementing the TCG spec
Name:           tpm2-abrmd
Version:        2.3.3
Release:        3%{?dist}
License:        BSD 2-Clause
URL:            https://github.com/tpm2-software/tpm2-abrmd
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        %{name}-%{version}.tar.gz
%define sha512 tpm2=2191c7e466271cb85fcb20fcd91c78df80f53030fb055d0b4670db33708939b60a9124955356f27662975abdcb9c8d144df884003986ffdbd801ca4e47edc21a

BuildRequires: which
BuildRequires: dbus-devel
BuildRequires: glib-devel >= 2.68.4
BuildRequires: tpm2-tss-devel

Requires: dbus
Requires: glib >= 2.68.4
Requires: tpm2-tss

%description
TPM2 Access Broker & Resource Management Daemon implementing the TCG spec

%package devel
Summary:     The libraries and header files needed for TSS2 ABRMD development.
Requires:    %{name} = %{version}-%{release}
%description devel
The libraries and header files needed for TSS2 ABRMD development.

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --with-systemdsystemunitdir=/usr/lib/systemd/system \
    --with-dbuspolicydir=/etc/dbus-1/system.d

make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/dbus-1/system.d/tpm2-abrmd.conf
%{_sbindir}/tpm2-abrmd
%{_libdir}/libtss2-tcti-tabrmd.so.0.0.0
%{_libdir}/systemd/system/tpm2-abrmd.service
%{_libdir}/systemd/system-preset/tpm2-abrmd.preset
%{_datadir}/dbus-1/*
%{_mandir}/man8

%files devel
%defattr(-,root,root)
%{_includedir}/tss2/*
%{_libdir}/pkgconfig/*
%{_libdir}/libtss2-tcti-tabrmd.so
%{_libdir}/libtss2-tcti-tabrmd.so.0
%{_mandir}/man3
%{_mandir}/man7

%changelog
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.3.3-3
- Bump version as part of glib upgrade
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.3.3-2
- Remove .la files
* Tue Aug 18 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.3-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.2-1
- Automatic Version Bump
* Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.1.0-1
- Initial build. First version
