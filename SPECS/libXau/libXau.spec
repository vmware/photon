Summary:        X11 Authorization Protocol library.
Name:           libXau
Version:        1.0.9
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512  libXau=3ca454ba466a807ea28b0f715066d73dc76ad312697b121d43e4d5766215052e9b7ffb8fe3ed3e496fa3f2a13f164ac692ff85cc428e26731b679f0f06a1d562

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
* Tue Jul 12 2022 Shivani Agarwal <shivania2@vmware.com> 1.0.9-1
- upgrade to 1.0.9
* Fri May 15 2015 Alexey Makhalov <amakhalov@vmware.com> 1.0.8-1
- initial version
