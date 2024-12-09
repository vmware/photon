Summary:        A high performance C-based HTTP client library built upon the Apache Portable Runtime (APR) library
Name:           serf
Version:        1.3.9
Release:        12%{?dist}
URL:            https://serf.apache.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.apache.org/dist/serf/%{name}-%{version}.tar.bz2
%define sha512 serf=9f5418d991840a08d293d1ecba70cd9534a207696d002f22dbe62354e7b005955112a0d144a76c89c7f7ad3b4c882e54974441fafa0c09c4aa25c49c021ca75d

Source1: license.txt
%include %{SOURCE1}

Patch0: 0001-openssl-3.0.0-compatibility.patch

Requires: openldap

BuildRequires: python3-setuptools
BuildRequires: apr-devel
BuildRequires: apr-util-devel
BuildRequires: scons
BuildRequires: openssl-devel
BuildRequires: openldap-devel

%description
The Apache Serf library is a C-based HTTP client library built upon the Apache
Portable Runtime (APR) library. It multiplexes connections, running the
read/write communication asynchronously. Memory copies and transformations are
kept to a minimum to provide high performance operation.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}
Requires:       apr-devel
Requires:       apr-util-devel
%description    devel
It contains the libraries and header files to create serf applications.

%prep
%autosetup -p1

%build
sed -i "/Append/s:RPATH=libdir,::" SConstruct
sed -i "/Default/s:lib_static,::" SConstruct
sed -i "/Alias/s:install_static,::" SConstruct
sed -i "/  print/{s/print/print(/; s/$/)/}" SConstruct
sed -i "/get_contents()/s/,/.decode()&/" SConstruct
scons PREFIX=%{_prefix}

%install
scons PREFIX=%{buildroot}%{_prefix} install

%if 0%{?with_check}
%check
scons check
%endif

%files
%defattr(-,root,root)
%{_libdir}/libserf-1.so.*

%files devel
%{_includedir}/*
%{_libdir}/libserf-1.so
%{_libdir}/pkgconfig/*

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.3.9-12
- Release bump for SRP compliance
* Tue Sep 10 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 1.3.9-11
- Bump version as a part of apr upgrade
* Fri Sep 29 2023 Nitesh Kumar <kunitesh@vmware.com> 1.3.9-10
- Bump version as a part of apr-util v1.6.3 upgrade
* Tue Sep 19 2023 Nitesh Kumar <kunitesh@vmware.com> 1.3.9-9
- Bump version as a part of openldap v2.6.4 upgrade
* Fri May 19 2023 Srish Srinivasan <ssrish@vmware.com> 1.3.9-8
- Bump version as a part of apr version upgrade
* Wed Feb 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.3.9-7
- Bump version as a part of openldap upgrade
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.3.9-6
- Update release to compile with python 3.11
* Sun Aug 01 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.3.9-5
- openssl 3.0.0 compatibility
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.3.9-4
- openssl 1.1.1
* Sat Aug 15 2020 Tapas Kundu <tkundu@vmware.com> 1.3.9-3
- Add setuptools in requires
* Mon Jul 06 2020 Tapas Kundu <tkundu@vmware.com> 1.3.9-2
- Build with python3
- Mass removal python2
- Remove static
* Mon Jan 22 2018 Xiaolin Li <xiaolinl@vmware.com> 1.3.9-1
- Initial build. First version
