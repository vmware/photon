Summary:        C based http parser for high performance applications.
Name:           http-parser
Version:        2.9.4
Release:        2%{?dist}
URL:            https://github.com/nodejs/http-parser
Source0:        %{name}-v%{version}.tar.gz
%define sha512  http-parser=b45df7b94d1c51079d44687d0a7f901f44faae51df4e84c7e3fe38f130c2d809d0e7c2a146c57b3723e60732aededc246bf44eadb10a95b710963d641f9fe7cd

Source1: license.txt
%include %{SOURCE1}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  gcc

%description
This is a parser for HTTP messages written in C. It parses both requests and responses. The parser is designed to be used in performance HTTP applications. It does not make any syscalls nor allocations, it does not buffer data, it can be interrupted at anytime.

%package devel
Summary:        http-parser devel
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
%description devel
This contains development tools and libraries for http-parser.

%prep
%autosetup -p1

%build
make PREFIX=%{_prefix} %{?_smp_mflags}

%install
make PREFIX="%{_prefix}" DESTDIR="%{buildroot}" install %{?_smp_mflags}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libhttp_parser.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/http_parser.h
%{_libdir}/libhttp_parser.so

%changelog
*    Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 2.9.4-2
-    Release bump for SRP compliance
*    Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.9.4-1
-    Automatic Version Bump
*    Fri Aug 03 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.8.1-1
-    Update to version 2.8.1 to get it to build with gcc 7.3
*    Wed Jul 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.1-1
-    Initial version of http-parser package for Photon.
