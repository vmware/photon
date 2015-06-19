Summary:	Hawkey
Name:		hawkey
Version:	2014.1
Release:	3%{?dist}
License:	LGPLv2+
URL:		http://fedoraproject.org/wiki/Features/Hawkey
Source0:	https://github.com/rpm-software-management/hawkey/archive/%{name}-%{version}.tar.gz
Group:		Development/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires: 	libsolv
BuildRequires: 	check
BuildRequires: 	cmake
BuildRequires: 	rpm
BuildRequires: 	rpm-devel
Requires:	libsolv

%description
Hawkey is a library allowing clients to query and resolve dependencies of RPM 
packages based on the current state of RPMDB and yum repositories.

%package devel
Summary:	A Library providing simplified C and Python API to libsolv
Group:		Development/Libraries
Requires:	hawkey = %{version}-%{release}
Provides:       pkgconfig(hawkey)

%description devel
Development files for hawkey.

%package -n python-hawkey
Summary:	Python 2 bindings for the hawkey library
Group:		Development/Languages
BuildRequires:  python2-devel
BuildRequires:  python2-libs
Requires:	%{name} = %{version}-%{release}
Requires:	python2

%description -n python-hawkey
Python 2 bindings for the hawkey library.

%prep
%setup -qn %{name}
%build
cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root)
%{_lib64dir}/libhawkey.so.*

%files -n python-hawkey
%defattr(-,root,root)
%{python_sitearch}/

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_lib64dir}/pkgconfig/*.pc
%{_lib64dir}/*.so
%exclude %{python_sitearch}/*

%changelog
*	Thu Jun 18 2015 Anish Swaminathan <anishs@vmware.com> 2014.1-3
-	Add pkgconfig Provides directive
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2014.1.1-2
-   Updated group.
*	Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 2014.1-1
-	Initial build. First version
