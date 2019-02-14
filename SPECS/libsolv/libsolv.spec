Summary:	Libsolv-0.6.19
Name:		libsolv
Version:	0.6.19
Release:	6%{?dist}
License:	BSD
URL:		https://github.com/openSUSE/libsolv
Source0:	https://github.com/openSUSE/libsolv/archive/%{name}-%{version}.tar.gz
%define sha1 libsolv=2066529e5a95aac15a79863bb937bb159b05cffa
Patch0:         CVE-2018-20532-20533-20534.patch
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
Requires:	libdb
Requires:	expat
BuildRequires:	libdb-devel
BuildRequires:	cmake
BuildRequires:	rpm-devel
BuildRequires:	expat
%description
Libsolv is a free package management library, using SAT technology to solve requests. 
It supports debian, rpm, archlinux and haiku style distributions. 
%prep
%setup -q
%patch0 -p1
%build
cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DRPM5=ON \
	-DENABLE_RPMDB=ON \
	-DENABLE_COMPLEX_DEPS=ON
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
*   Thu Feb 14 2019 Keerthana K <keerthanak@vmware.com> 0.6.19-6
-   Fix for CVE-2018-20532, CVE-2018-20533, CVE-2018-20534.
*   Wed Jul 18 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6.19-5
-   use libdb
*   Sat Sep 30 2017 Anish Swaminathan <anishs@vmware.com> 0.6.19-4
-   Release bump for expat version update
*   Fri Sep 29 2017 Alexey Makhalov <amakhalov@vmware.com> 0.6.19-3
-   added compile flag to support rich dependencies
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6.19-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  0.6.19-1
-   Upgrade to 0.6.19
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 0.6.17-1
-   Updated to version 0.6.17
*   Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.6.6-3
-   Updated build-requires after creating devel package for db. 
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 0.6.6-2
-   Updated group.
*   Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 0.6.6-1
-   Initial build. First version
