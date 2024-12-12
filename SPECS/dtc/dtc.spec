Summary:       Device Tree Compiler
Name:          dtc
Version:       1.6.1
Release:       3%{?dist}
URL:           https://devicetree.org
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: https://www.kernel.org/pub/software/utils/%{name}/%{name}-%{version}.tar.gz
%define sha512 %{name}=34b64f356070710fd78f34ed624a06cec02915c98ab53eddbb0843f2a4c62dc95a78aa8583d7f433db60d1233eb1a2babecd85cd8179e74f27fe46ca412cb2b3

Source1: license.txt
%include %{SOURCE1}

BuildRequires: build-essential
BuildRequires: swig

%description
Devicetree is a data structure for describing hardware. Rather than hard coding
every detail of a device into an operating system, many aspects of the hardware
can be described in a data structure that is passed to the operating system at
boot time. The devicetree is used by OpenFirmware, OpenPOWER Abstraction Layer
(OPAL), Power Architecture Platform Requirements (PAPR) and in the standalone
Flattened Device Tree (FDT) form.

%package devel
Summary:    Development headers for device tree library
Requires:   %{name} = %{version}-%{release}

%description devel
This package provides development files for libfdt

%prep
%autosetup -p1

%build
%make_build

%install
%make_install %{?_smp_mflags} \
        DESTDIR=%{buildroot} PREFIX=%{_prefix} \
        LIBDIR=%{_libdir} BINDIR=%{_bindir} INCLUDEDIR=%{_includedir}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license GPL
%doc Documentation/manual.txt
%{_bindir}/*
%{_libdir}/libfdt-%{version}.so
%{_libdir}/libfdt.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/libfdt.so
%{_libdir}/libfdt.a
%{_includedir}/*

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.6.1-3
- Release bump for SRP compliance
* Thu Jan 12 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.6.1-2
- Bump up version no. as part of swig upgrade
* Fri Aug 19 2022 Ajay Kaher <akaher@vmware.com> 1.6.1-1
- Version update
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.0-1
- Automatic Version Bump
* Wed Jul 24 2019 Ajay Kaher <akaher@vmware.com> 1.5.0-1
- Initial build. First version
