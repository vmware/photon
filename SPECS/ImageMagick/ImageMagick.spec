%global VER 7.1.0
%global Patchlevel 47
%global major_version 7

Name:           ImageMagick
Version:        7.1.0.47
Release:        4%{?dist}
Summary:        An X application for displaying and manipulating images
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        ImageMagick
Url:            http://www.imagemagick.org

Source0: https://www.imagemagick.org/download/%{name}-%{VER}-%{Patchlevel}.tar.gz
%define sha512 %{name}=dae53c80b1fec69e8a570e82553197e2a9f3b1d0dd9b7cdf30e2731e044a83bef82912a5d339c0470d1e41bdf343f2cbd97376d2ef986d33c05bc6c87a705d0d

Requires:       %{name}-libs = %{version}-%{release}
Requires:       libgomp
Requires:       bzip2-libs
Requires:       glibc
Requires:       zlib

%description
ImageMagick is an image display and manipulation tool for the X
Window System. ImageMagick can read and write JPEG, TIFF, PNM, GIF,
and Photo CD image formats. It can resize, rotate, sharpen, color
reduce, or add special effects to an image, and when finished you can
either save the completed work in the original format or a different
one. ImageMagick also includes command line programs for creating
animated or transparent .gifs, creating composite images, creating
thumbnail images, and more.

ImageMagick is one of your choices if you need a program to manipulate
and display images. If you want to develop your own applications
which use ImageMagick code or APIs, you need to install
ImageMagick-devel as well.

%package        devel
Summary:        Library links and header files for ImageMagick app development
Requires:       pkg-config
Requires:       %{name} = %{version}-%{release}

%description    devel
ImageMagick-devel contains the library links and header files you'll
need to develop ImageMagick applications. ImageMagick is an image
manipulation program.

If you want to create applications that will use ImageMagick code or
APIs, you need to install ImageMagick-devel as well as ImageMagick.
You do not need to install it if you just want to use ImageMagick,
however.

%package        libs
Summary:        ImageMagick libraries to link with

%description    libs
This packages contains a shared libraries to use within other applications.

%package        doc
Summary:        ImageMagick html documentation

%description    doc
ImageMagick documentation, this package contains usage (for the
commandline tools) and API (for the libraries) documentation in html format.
Note this documentation can also be found on the ImageMagick website:
http://www.imagemagick.org/

%package        c++
Summary:        ImageMagick Magick++ library (C++ bindings)
Requires:       %{name}-libs = %{version}-%{release}
Requires:       libstdc++
Requires:       libgomp
Requires:       bzip2-libs
Requires:       glibc
Requires:       zlib

%description    c++
This package contains the Magick++ library, a C++ binding to the ImageMagick
graphics manipulation library.

Install ImageMagick-c++ if you want to use any applications that use Magick++.

%package        c++-devel
Summary:        C++ bindings for the ImageMagick library
Requires:       %{name}-libs = %{version}-%{release}
Requires:       %{name}-devel = %{version}-%{release}
Requires:       pkg-config

%description    c++-devel
ImageMagick-devel contains the static libraries and header files you'll
need to develop ImageMagick applications using the Magick++ C++ bindings.
ImageMagick is an image manipulation program.

If you want to create applications that will use Magick++ code
or APIs, you'll need to install ImageMagick-c++-devel, ImageMagick-devel and
ImageMagick.
You don't need to install it if you just want to use ImageMagick, or if you
want to develop/compile applications using the ImageMagick C interface,
however.

%prep
%autosetup -p1 -n %{name}-%{VER}-%{Patchlevel}

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

rm %{buildroot}%{_libdir}/*.a

%if 0%{?with_check}
%check
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}
%make_build check
rm PerlMagick/demo/Generic.ttf
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/[a-z]*
%{_mandir}/man[145]/[a-z]*
%{_mandir}/man1/%{name}.*

%files doc
%defattr(-,root,root)
%doc %{_datadir}/doc/%{name}-%{major_version}/*

%files libs
%defattr(-,root,root)
%{_libdir}/libMagickCore-%{major_version}.Q16HDRI.so.10*
%{_libdir}/libMagickWand-%{major_version}.Q16HDRI.so.10*
%{_libdir}/%{name}-%{VER}
%{_datadir}/%{name}-%{major_version}
%dir %{_sysconfdir}/%{name}-%{major_version}
%config(noreplace) %{_sysconfdir}/%{name}-%{major_version}/*.xml

%files c++-devel
%defattr(-,root,root)
%{_bindir}/Magick++-config
%{_includedir}/%{name}-%{major_version}/Magick++
%{_includedir}/%{name}-%{major_version}/Magick++.h
%{_libdir}/libMagick++-%{major_version}.Q16HDRI.so
%{_libdir}/pkgconfig/Magick++.pc
%{_libdir}/pkgconfig/Magick++-%{major_version}.Q16HDRI.pc
%{_mandir}/man1/Magick++-config.*

%files devel
%defattr(-,root,root)
%{_bindir}/MagickCore-config
%{_bindir}/MagickWand-config
%{_libdir}/libMagickCore-%{major_version}.Q16HDRI.so
%{_libdir}/libMagickWand-%{major_version}.Q16HDRI.so
%{_libdir}/pkgconfig/MagickCore.pc
%{_libdir}/pkgconfig/MagickCore-%{major_version}.Q16HDRI.pc
%{_libdir}/pkgconfig/ImageMagick.pc
%{_libdir}/pkgconfig/ImageMagick-%{major_version}.Q16HDRI.pc
%{_libdir}/pkgconfig/MagickWand.pc
%{_libdir}/pkgconfig/MagickWand-%{major_version}.Q16HDRI.pc
%dir %{_includedir}/%{name}-%{major_version}
%{_includedir}/%{name}-%{major_version}/MagickCore/*
%{_includedir}/%{name}-%{major_version}/MagickWand/*
%{_mandir}/man1/MagickCore-config.*
%{_mandir}/man1/MagickWand-config.*

%files c++
%defattr(-,root,root)
%{_libdir}/libMagick++-%{major_version}.Q16HDRI.so.5*

%changelog
* Tue Jun 06 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.1.0.47-4
- Fix spec issues
* Fri May 05 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.1.0.47-3
- Remove _isa entries
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 7.1.0.47-2
- Bump version as a part of zlib upgrade
* Mon Aug 29 2022 Shivani Agarwal <shivania2@vmware.com> 7.1.0.47-1
- Upgrade version to 7.1.0.47
* Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 7.1.0.35-1
- Automatic Version Bump
* Tue May 17 2022 Shivani Agarwal <shivania2@vmware.com> 7.1.0.19-1
- Fix for CVE-2022-1114
* Tue Jun 22 2021 Piyush Gupta <gpiyush@vmware.com> 7.1.0.1-1
- Initial build for Photon.
