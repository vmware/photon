Summary:        C library for manipulating tar files
Name:           libtar
Version:        1.2.20
Release:        8%{?dist}
URL:            https://github.com/tklauser/libtar
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/tklauser/libtar/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=11a12695abf4f9668801d24b7b552daed1219b2f395c09818d15e16721f7136d63aa0c09e442401e4fedbf7335748f0dc46f8da21b94b36595910b2fe44d4aea

Source1: license.txt
%include %{SOURCE1}

Patch0:         libtar-gen-debuginfo.patch
Patch1:         libtar-CVE-2013-4420.patch
Patch2:         libtar-CVE-2021-33643-CVE-2021-33644.patch
Patch3:         libtar-CVE-2021-33645-CVE-2021-33646.patch

Provides:       libtar.so.0()(64bit)

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
# Using autosetup is not feasible
%setup
%patch0
%patch1 -p1
%patch2 -p1
%patch3 -p1

autoreconf -iv

%build
%configure CFLAGS="%{optflags}" STRIP=/bin/true --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

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

%changelog
* Wed Dec 11 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.2.20-8
- Release bump for SRP compliance
* Tue May 16 2023 Shivani Agarwal <shivania2@vmware.com> 1.2.20-7
- Fix CVE-2021-33643, CVE-2021-33644, CVE-2021-33645, CVE-2021-33646
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.2.20-6
- Remove .la files
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
