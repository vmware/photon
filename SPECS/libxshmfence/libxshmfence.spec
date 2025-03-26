Summary:        X11 libxshmfence runtime library.
Name:           libxshmfence
Version:        1.3.2
Release:        3%{?dist}
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  pkg-config
BuildRequires:  util-macros
BuildRequires:  proto

%description
The X11 Shared Memory fences library.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       pkg-config
Requires:       util-macros
Requires:       libX11-devel
Requires:       proto

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name \*.la -delete

%check
make check %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/

%changelog
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.3.2-3
- Release bump for SRP compliance
* Wed Jan 03 2024 Anmol Jain <anmol.jain@broadcom.com> 1.3.2-2
- Fix for test failure
* Thu Feb 23 2023 Shivani Agarwal <shivania2@vmware.com> 1.3.2-1
- Version update
* Tue Aug 03 2021 Alexey Makhalov <amakhalov@vmware.com> 1.3-1
- Version update
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.2-1
- initial version
