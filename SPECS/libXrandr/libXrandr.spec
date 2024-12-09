Summary:        X11 Xrandr runtime library.
Name:           libXrandr
Version:        1.5.2
Release:        2%{?dist}
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%define sha512  libXrandr=fcd005f9839e7ef980607128a5d76d7b671cc2f5755949e03c569c500d7e987cb3f6932750ab8bf6e2c1086ec69dde09d5831f0c2098b9f9ad46be4f56db0d87

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libXrender-devel
BuildRequires:  libXext-devel
Requires:       libXrender
Requires:       libXext

%description
The X11 libXrandr library.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libXrender-devel
Requires:       libXext-devel

%description    devel
X.Org X11 libXrandr development package

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}
find %{buildroot} -name \*.la -delete

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
%{_libdir}/pkgconfig
%{_datadir}/*

%changelog
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.5.2-2
- Release bump for SRP compliance
* Tue Jul 12 2022 Shivani Agarwal <shivania2@vmware.com> 1.5.2-1
- Upgrade to 1.5.2
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 1.4.2-1
- initial version
