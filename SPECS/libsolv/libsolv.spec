Summary:	Libsolv-0.6.6
Name:		libsolv
Version:	0.6.6
Release:	1
License:	BSD
URL:		http://www.cmake.org/
Source0:	https://github.com/openSUSE/libsolv/archive/%{name}-%{version}.tar.gz
Group:		GeneralUtilities
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
*	Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 0.6.6-1
-	Initial build. First version
