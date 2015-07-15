Summary:	Libsolv-0.6.6
Name:		libsolv
Version:	0.6.6
Release:	2%{?dist}
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
BuildRequires:	db
BuildRequires:	cmake
BuildRequires:	rpm-devel
BuildRequires:	expat
%description
Libsolv is a free package management library, using SAT technology to solve requests. 
It supports debian, rpm, archlinux and haiku style distributions. 
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
%{_lib64dir}/*
/usr/share/*
%{_includedir}/*
%changelog
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 0.6.6-2
-   Updated group.
*	Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 0.6.6-1
-	Initial build. First version
