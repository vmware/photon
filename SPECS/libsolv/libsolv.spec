Summary:        Libsolv-0.6.19
Name:           libsolv
Version:        0.6.26
Release:        2%{?dist}
License:        BSD
URL:            https://github.com/openSUSE/libsolv
Source0:        https://github.com/openSUSE/libsolv/archive/%{name}-%{version}.tar.gz
%define sha1    libsolv=7699af00e648bf3e631246559c48ceb7f3f544b9
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       libdb
Requires:       expat-libs
BuildRequires:  libdb-devel
BuildRequires:  cmake
BuildRequires:  rpm-devel
BuildRequires:  expat-devel
%description
Libsolv is a free package management library, using SAT technology to solve requests. 
It supports debian, rpm, archlinux and haiku style distributions.

%package devel
Summary:        Development headers for libsolv
Requires:       %{name} = %{version}-%{release}

%description devel
The libsolv-devel package contains libraries, header files and documentation
for developing applications that use libsolv.

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
make %{?_smp_mflags} test

%files
%defattr(-,root,root)
%{_bindir}/*
%{_lib64dir}/libsolv.so.*
%{_lib64dir}/libsolvext.so.*
%{_mandir}/man1/*


%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_lib64dir}/libsolv.so
%{_lib64dir}/libsolvext.so
%{_lib64dir}/pkgconfig/*
%{_datadir}/cmake/*
%{_mandir}/man3/*

%changelog
*   Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 0.6.26-2
-   libsolv requires expat-libs.
*   Tue Apr 04 2017 Kumar Kaushik <kaushikk@vmware.com>  0.6.26-1
-   Upgrade to 0.6.26
*   Mon Dec 19 2016 Xiaolin Li <xiaolinl@vmware.com> 0.6.19-4
-   Added -devel subpackage.
*   Thu Oct 27 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6.19-3
-   use libdb
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
