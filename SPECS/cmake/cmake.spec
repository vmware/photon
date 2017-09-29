Summary:	Cmake-3.8.0
Name:		cmake
Version:	3.8.0
Release:	4%{?dist}
License:	BSD and LGPLv2+
URL:		http://www.cmake.org/
Source0:	http://www.cmake.org/files/v3.8/%{name}-%{version}.tar.gz
Patch0:         disableUnstableUT.patch
%define sha1 cmake=660ec06a46b46dc5d675371a2256ec739f8bb8b7
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

make
%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
make  %{?_smp_mflags} test

%files
%defattr(-,root,root)
/usr/share/%{name}-*/*
%{_bindir}/*
/usr/doc/%{name}-*/*
/usr/share/aclocal/*
%changelog
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
