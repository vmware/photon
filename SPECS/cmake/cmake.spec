Summary:	Cmake-3.4.3
Name:		cmake
Version:	3.4.3
Release:	3%{?dist}
License:	BSD and LGPLv2+
URL:		http://www.cmake.org/
Source0:	http://www.cmake.org/files/v3.4/%{name}-%{version}.tar.gz
%define sha1 cmake=49e4f05d46d4752e514b19ba36bf97d20a7da66a
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	ncurses-devel
Requires:	ncurses
%description
CMake is an extensible, open-source system that manages the build process in an 
operating system and in a compiler-independent manner. 
%prep
%setup -q
%build
./bootstrap --prefix=%{_prefix}
make %{?_smp_mflags}
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
*       Thu Oct 06 ChangLee <changlee@vmware.com> 3.4.3-3
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
