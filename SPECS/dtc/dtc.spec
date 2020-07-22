Summary:       Device Tree Compiler
Name:          dtc
Version:       1.6.0
Release:       1%{?dist}
License:       GPLv2+
URL:           https://devicetree.org/
Group:         Development/Tools
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       https://www.kernel.org/pub/software/utils/%{name}/%{name}-%{version}.tar.gz
%define sha1 dtc=ef037f4599b7b1e883c9bb588b24d289dc9cd1f2
BuildRequires: gcc make
BuildRequires: flex bison swig

%description
Devicetree is a data structure for describing hardware. Rather than hard coding
every detail of a device into an operating system, many aspects of the hardware
can be described in a data structure that is passed to the operating system at
boot time. The devicetree is used by OpenFirmware, OpenPOWER Abstraction Layer
(OPAL), Power Architecture Platform Requirements (PAPR) and in the standalone
Flattened Device Tree (FDT) form.

%package devel
Summary: Development headers for device tree library
Requires: %{name} = %{version}-%{release}

%description devel
This package provides development files for libfdt

%prep
%setup -q
sed -i 's/python2/python3/' pylibfdt/setup.py

%build
make %{?_smp_mflags} V=1 CC="gcc $RPM_OPT_FLAGS $RPM_LD_FLAGS"

%install
make install DESTDIR=%{buildroot} PREFIX=%{buildroot}/usr \
                            LIBDIR=%{_libdir} BINDIR=%{_bindir} INCLUDEDIR=%{_includedir} V=1

%clean
rm -rf %{buildroot}/*

%files
%license GPL
%doc Documentation/manual.txt
%{_bindir}/*
%{_libdir}/libfdt-%{version}.so
%{_libdir}/libfdt.so.*

%files devel
%{_libdir}/libfdt.so
%{_libdir}/libfdt.a
%{_includedir}/*

%changelog
* Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.0-1
- Automatic Version Bump
* Wed Jul 24 2019 Ajay Kaher <akaher@vmware.com> 1.5.0-1
- Initial build. First version
