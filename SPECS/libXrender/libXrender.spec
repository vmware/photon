%global build_if %{photon_subrelease} >= 91

Summary:        X11 Xrender runtime library.
Name:           libXrender
Version:        0.9.12
Release:        2%{?dist}
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  libX11-devel
Requires:       libX11
Provides:       pkgconfig(xrender)

%description
The X11 Renderer library.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libX11-devel

%description    devel
X.Org X11 libXrender development package

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
%{_libdir}/pkgconfig
%{_libdir}/*.a
%{_libdir}/*.so
%{_datadir}/*

%changelog
* Sat Aug 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.9.12-2
- Extend to build for 91 and above
* Tue Jul 28 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.9.12-1
- Upgrade to 0.9.12
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 0.9.10-3
- Release bump for SRP compliance
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 0.9.10-2
- Bump version as a part of libX11 upgrade
* Tue Jul 12 2022 Shivani Agarwal <shivania2@vmware.com> 0.9.10-1
- Upgrade to 0.9.10
* Tue May 19 2015 Alexey Makhalov <amakhalov@vmware.com> 0.9.8-1
- initial version
