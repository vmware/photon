Summary:        TPM2 Access Broker & Resource Management Daemon implementing the TCG spec
Name:           tpm2-abrmd
Version:        2.4.1
Release:        1%{?dist}
License:        BSD 2-Clause
URL:            https://github.com/tpm2-software/tpm2-abrmd
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha512  tpm2=0335285678cfceca4f185981ded90d213ff796cadddc9b5d6dbf2db533f81023a0f1089bbd8a8017bccb95190889be23b24d38a176d3368d221479aff4ff7d6c
BuildRequires:	which dbus-devel glib-devel tpm2-tss-devel
Requires:       dbus glib tpm2-tss

%description
TPM2 Access Broker & Resource Management Daemon implementing the TCG spec

%package        devel
Summary:        The libraries and header files needed for TSS2 ABRMD development.
Requires:       %{name} = %{version}-%{release}

%description    devel
The libraries and header files needed for TSS2 ABRMD development.

%prep
%autosetup

%build
%configure \
    --disable-static \
    --with-systemdsystemunitdir=/usr/lib/systemd/system \
    --with-dbuspolicydir=/etc/dbus-1/system.d
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install

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
%{_libdir}/libtss2-tcti-tabrmd.la
%{_libdir}/libtss2-tcti-tabrmd.so
%{_libdir}/libtss2-tcti-tabrmd.so.0
%{_mandir}/man3
%{_mandir}/man7

%changelog
*   Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 2.4.1-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.4.0-1
-   Automatic Version Bump
*   Tue Aug 18 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.3-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.2-1
-   Automatic Version Bump
*   Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.1.0-1
-   Initial build. First version.
