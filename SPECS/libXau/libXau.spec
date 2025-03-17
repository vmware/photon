Summary:        X11 Authorization Protocol library.
Name:           libXau
Version:        1.0.9
Release:        2%{?dist}
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

BuildRequires: proto

%description
The libXau package contains a library implementing the X11 Authorization Protocol. This is useful for restricting client access to the display.

%package        devel
Summary:        Header and development files for libXau
Requires:       %{name} = %{version}-%{release}
Requires:       proto

%description    devel
X.Org X11 libXau development package

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name \*.la -delete

%ldconfig_scriptlets

%check
make %{?_smp_mflags} -k check |& tee %{_specdir}/%{name}-check-log

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/libXau.so.*

%files devel
%defattr(-,root,root)
%{_mandir}/*
%{_includedir}/*
%{_libdir}/libXau.a
%{_libdir}/pkgconfig
%{_libdir}/*.so

%changelog
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.0.9-2
- Release bump for SRP compliance
* Tue Jul 12 2022 Shivani Agarwal <shivania2@vmware.com> 1.0.9-1
- upgrade to 1.0.9
* Fri May 15 2015 Alexey Makhalov <amakhalov@vmware.com> 1.0.8-1
- initial version
