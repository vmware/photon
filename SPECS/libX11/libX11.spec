Summary:        Core X11 protocol client library.
Name:           libX11
Version:        1.8.5
Release:        1%{?dist}
License:        MIT
URL:            http://www.x.org/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/freedesktop/xorg-libX11/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=967f7746b08650c4238630b007137e89085c88d89b256d5d9b37faa6a50b1df2a3ec749281677f1c64570a3eafd310872e6842cbb5aecaba1cdf7c0c4140ea56
Patch0:         CVE-2023-3138.patch

BuildRequires:  libxcb-devel
BuildRequires:  xtrans

Requires:       fontconfig
Requires:       libxcb
Requires:       libXau
Requires:       libXdmcp
Provides:       pkgconfig(x11)

%description
Core X11 protocol client library.

%package        devel
Summary:        Header and development files for libX11
Requires:       %{name} = %{version}-%{release}
Requires:       libxcb-devel
Requires:       xtrans

%description    devel
X.Org X11 libX11 development package

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
%{_datadir}/X11/
%{_mandir}/man5/

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/pkgconfig/
%{_libdir}/*.so
%{_docdir}/
%{_mandir}/man3/

%changelog
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 1.8.5-1
- Upgrade to 1.8.5 to Fix CVE-2023-3138
* Tue Jul 12 2022 Shivani Agarwal <shivania2@vmware.com> 1.8.1-1
- Upgrade to 1.8.1
* Wed Jul 03 2019 Alexey Makhalov <amakhalov@vmware.com> 1.6.3-3
- Locale support
* Wed Nov 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.6.3-2
- Updated build requires & requires to build with Photon 2.0
* Mon May 18 2015 Alexey Makhalov <amakhalov@vmware.com> 1.6.3-1
- initial version
