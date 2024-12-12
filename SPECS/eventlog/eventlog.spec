Summary:    Syslog event logger library
Name:       eventlog
Version:    0.2.12
Release:    5%{?dist}
URL:        https://www.balabit.com
Group:      System Environment/Daemons
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://www.balabit.com/downloads/files/eventlog/0.2/%{name}_%{version}.tar.gz
%define sha512 %{name}=a681ab2961f5bf38e106a5b0b4492e74098808e2bf1a100f545736902649c705db124c0847796a47485faa8b0befe691a789d752f313c5b65ad50ed2763d2cce

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  bison
BuildRequires:  flex

%description
The EventLog library aims to be a replacement of the simple syslog() API
provided on UNIX systems. The major difference between EventLog and syslog
is that EventLog tries to add structure to messages.

EventLog provides an interface to build, format and output an event record.
The exact format and output method can be customized by the administrator
via a configuration file.

This package is the runtime part of the library.

%package devel
Summary:    Development libraries & headers for %{name}
Requires:   %{name} = %{version}-%{release}

%description devel
Development libraries & headers for %{name}

%prep
%autosetup -p1

%build
%configure --disable-silent-rules
%make_build

%install
%make_install

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/eventlog/*.h
%{_libdir}/pkgconfig/eventlog.pc

%changelog
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.2.12-5
- Release bump for SRP compliance
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.2.12-4
- Remove .la files
- Introduce devel package
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.2.12-3
- Use standard configure macros
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.2.12-2
- GA - Bump release of all rpms
* Fri Jun 5 2015 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.12-1
- Add eventlog library for syslog-ng to photon
