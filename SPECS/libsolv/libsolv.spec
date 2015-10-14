Summary:	Libsolv-0.6.6
Name:		libsolv
Version:	0.6.6
Release:	4%{?dist}
License:	BSD
URL:		http://www.cmake.org/
Source0:	https://github.com/openSUSE/libsolv/archive/%{name}-%{version}.tar.gz
%define sha1 libsolv=dca7ddcc42932a87c5a22196c50cad549f16e414
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
Requires:	db
Requires:	rpm
Requires:	expat
BuildRequires:	db-devel
BuildRequires:	cmake
BuildRequires:	rpm-devel
BuildRequires:	expat-devel
%description
Libsolv is a free package management library, using SAT technology to solve requests. 
It supports debian, rpm, archlinux and haiku style distributions. 

%package devel
Summary: Development libraries and header files for the libsolv library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
libsolv-devel contains the development libraries and header files for
libsolv.

%prep
%setup -q
%build
cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DRPM5=ON
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
%defattr(-,root,root)
%{_bindir}/*
%{_lib64dir}/*.so.*
/usr/share/man/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_lib64dir}/*.so
/usr/share/cmake/*

%changelog
*   Wed Oct 14 2015 Xiaolin Li <xiaolinl@vmware.com> 0.6.6-4
-   Move development libraries and header files to devel package.
* 	Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.6.6-3
-	Updated build-requires after creating devel package for db. 
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 0.6.6-2
-   Updated group.
*	Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 0.6.6-1
-	Initial build. First version
