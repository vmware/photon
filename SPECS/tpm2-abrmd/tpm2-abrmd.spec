Summary:	TPM2 Access Broker & Resource Management Daemon implementing the TCG spec
Name:		tpm2-abrmd
Version:	2.1.0
Release:	1%{?dist}
License:	BSD 2-Clause
URL:		https://github.com/tpm2-software/tpm2-tools
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	%{name}-%{version}.tar.gz
%define sha1 tpm2=0a1c72bf0b2d2511191425c62b9258e65c84c4db
BuildRequires:	which dbus-devel glib-devel tpm2-tss-devel
Requires:	dbus glib tpm2-tss
%description
TPM2 Access Broker & Resource Management Daemon implementing the TCG spec

%package devel
Summary:    The libraries and header files needed for TSS2 ABRMD development.
Requires:   %{name} = %{version}-%{release}
%description devel
The libraries and header files needed for TSS2 ABRMD development.

%prep
%setup -q
%build
%configure \
    --disable-static \
    --with-systemdsystemunitdir=/usr/lib/systemd/system \
    --with-dbuspolicydir=/etc/dbus-1/system.d

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

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
*   Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.1.0-1
-   Initial build. First version
