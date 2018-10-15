Summary:	Cmake-3.12.1
Name:		cmake
Version:	3.12.1
Release:	2%{?dist}
License:	BSD and LGPLv2+
URL:		http://www.cmake.org/
Source0:	http://www.cmake.org/files/v3.12/%{name}-%{version}.tar.gz
%define sha1 cmake=5359cd2e36051b0746580298d42518b0aef27979
Source1:	macros.cmake
Patch0:         disableUnstableUT.patch
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	ncurses-devel
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  curl
BuildRequires:  curl-devel
BuildRequires:  libgcc-devel
BuildRequires:  expat-libs
BuildRequires:  expat-devel
Requires:	ncurses
Requires:       expat
%description
CMake is an extensible, open-source system that manages the build process in an 
operating system and in a compiler-independent manner. 
%prep
%setup -q
%patch0 -p1
%build
ncores="$(/usr/bin/getconf _NPROCESSORS_ONLN)"
./bootstrap --prefix=%{_prefix} --system-expat --parallel=$ncores
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
install -Dpm0644 %{SOURCE1} %{buildroot}%{_libdir}/rpm/macros.d/macros.cmake

%check
make  %{?_smp_mflags} test

%files
%defattr(-,root,root)
/usr/share/%{name}-*/*
%{_bindir}/*
/usr/doc/%{name}-*/*
/usr/share/aclocal/*
%{_libdir}/rpm/macros.d/macros.cmake

%changelog
*       Sun Sep 30 2018 Bo Gan <ganb@vmware.com> 3.12.1-2
-       smp make (make -jN)
-       specify /usr/lib as CMAKE_INSTALL_LIBDIR
*       Fri Sep 07 2018 Ajay Kaher <akaher@vmware.com> 3.12.1-1
-       Upgrading version to 3.12.1
-       Adding macros.cmake
*       Fri Sep 29 2017 Kumar Kaushik <kaushikk@vmware.com> 3.8.0-4
-       Building using system expat libs.
*       Thu Aug 17 2017 Kumar Kaushik <kaushikk@vmware.com> 3.8.0-3
-       Fixing make check bug # 1632102.
*	Tue May 23 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.8.0-2
-	bug 1448414: Updated to build in parallel
*       Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com>  3.8.0-1
-       Upgrade to 3.8.0
*       Thu Oct 06 2016 ChangLee <changlee@vmware.com> 3.4.3-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.4.3-2
-	GA - Bump release of all rpms
*       Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 3.4.3-1
-       Updated version.
*       Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 3.2.1.2
-       Updated group.
*	Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2.1-1
-	Update to 3.2.1
*	Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 3.0.2-1
-	Initial build. First version
