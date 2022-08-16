Summary:        C library for manipulating tar files
Name:           libtar
Version:        1.2.20
Release:        6%{?dist}
URL:            https://github.com/tklauser/libtar/archive/v1.2.20.tar.gz
License:        MIT
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha512 libtar=11a12695abf4f9668801d24b7b552daed1219b2f395c09818d15e16721f7136d63aa0c09e442401e4fedbf7335748f0dc46f8da21b94b36595910b2fe44d4aea
Patch0:         libtar-gen-debuginfo.patch
Patch1:         libtar-1.2.11-missing-protos.patch
Patch2:         libtar-1.2.11-mem-deref.patch
Patch3:         libtar-1.2.20-fix-resource-leaks.patch
Patch4:         libtar-1.2.20-no-static-buffer.patch
Patch5:         libtar-CVE-2013-4420.patch
Patch6:         libtar-CVE-2021-33643-CVE-2021-33644.patch
Patch7:         libtar-CVE-2021-33645-CVE-2021-33646.patch

BuildRequires:  libtool

%description
libtar is a library for manipulating tar files from within C programs.

%package        devel
Summary:        Development files for libtar
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The litar-devel package contains libraries and header files for
developing applications that use libtar.

%prep
%autosetup -n %{name}-%{version} -p1
# set correct version for .so files
%global ltversion %(echo %{version} | tr '.' ':')
sed -i 's/-rpath $(libdir)/-rpath $(libdir) -version-number %{ltversion}/' lib/Makefile.in
autoreconf -iv

%build
%configure CFLAGS="%{optflags}" STRIP=/bin/true --disable-static
%make_build

%install
%make_install
chmod +x %{buildroot}/%{_libdir}/libtar.so.*

#%%check
#Commented out %check due to no test existence

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/libtar
%{_libdir}/libtar.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/libtar.so
%exclude %{_libdir}/libtar.la

%changelog
* Tue Aug 16 2022 Ankit Jain <ankitja@vmware.com> 1.2.20-6
- fix CVE-2021-33643 CVE-2021-33644 CVE-2021-33645 CVE-2021-33646
- fix multiple memory leak related issues
* Thu Nov 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.20-5
- Fix CVE-2013-4420
* Thu Jun 29 2017 Chang Lee <changlee@vmware.com> 1.2.20-4
- Removed %check due to no test existence.
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.20-3
- Ensure non empty debuginfo
* Fri Mar 10 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.20-2
- Provides libtar.so.0()(64bit).
* Fri Mar 03 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.20-1
- Initial packaging for Photon
