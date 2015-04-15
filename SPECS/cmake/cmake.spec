Summary:	Cmake-3.0.2
Name:		cmake
Version:	3.2.1
Release:	1
License:	BSD and LGPLv2+
URL:		http://www.cmake.org/
Source0:	http://www.cmake.org/files/v3.2/%{name}-%{version}.tar.gz
Group:		GeneralUtilities
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
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
%defattr(-,root,root)
/usr/share/%{name}-*/*
%{_bindir}/*
/usr/doc/%{name}-*/*
/usr/share/aclocal/*
%changelog
*	Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2.1-1
-	Update to 3.2.1
*	Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 3.0.2-1
-	Initial build. First version
