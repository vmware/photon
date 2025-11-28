Summary:    contains libraries for reading and writing PNG files.
Name:       libpng
Version:    1.6.51
Release:    1%{?dist}
License:    libpng
URL:        http://www.libpng.org/
Group:      System Environment/Libraries
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/pnggroup/libpng/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}=3b9b320b306388d0394404dbd6a978ba115743d913b4dd8d382b7ecf1f4e1979439e9829187058f52553f0aac0f73b274091a354c00286cdc699373b5c727fde

Provides:   pkgconfig(libpng)
Provides:   pkgconfig(libpng16)

%description
The libpng package contains libraries used by other programs for reading and writing PNG files. The PNG format was designed as a replacement for GIF and, to a lesser extent, TIFF, with many improvements and extensions and lack of patent problems.

%package    devel
Summary:    Header and development files
Requires:   %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure
make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}
rm -f %{buildroot}%{_libdir}/*.la

%check
make %{?_smp_mflags} -k check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/pngfix
%{_bindir}/png-fix-itxt
%{_libdir}/*.so.*
%{_datadir}/man/man5/*

%files devel
%defattr(-,root,root)
%{_bindir}/*-config
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*.pc
%{_datadir}/man/man3/*

%changelog
* Fri Nov 28 2025 Mukul Sikka <mukul.sikka@broadcom.com> 1.6.51-1
- Update to version 1.6.51
- Fix CVE-2025-64506, CVE-2025-65018, CVE-2025-64505, CVE-2025-64720
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.6.37-2
- Remove .la files
* Thu Mar 05 2020 Ashwin H <ashwinh@vmware.com> 1.6.37-1
- Update to 1.6.37
* Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 1.6.35-1
- Update to 1.6.35
* Tue Apr 11 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.6.29-1
- Updated to version 1.6.29
* Thu Feb 23 2017 Divya Thaluru <dthaluru@vmware.com> 1.6.27-1
- Updated to version 1.6.27
* Mon Sep 12 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.6.23-2
- Included the libpng16 pkgconfig
* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 1.6.23-1
- Initial version
