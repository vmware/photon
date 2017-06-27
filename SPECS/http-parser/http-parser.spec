Summary:	C based http parser for high performance applications.
Name:		http-parser
Version:	2.7.1
Release:	1%{?dist}
License:	MIT
URL:		https://github.com/nodejs/http-parser
Source0:	%{name}-v%{version}.tar.gz
%define sha1    http-parser=e122b1178ec5c9920186cc8293aca9eca7584b12
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildRequires:  gcc

%description
This is a parser for HTTP messages written in C. It parses both requests and responses. The parser is designed to be used in performance HTTP applications. It does not make any syscalls nor allocations, it does not buffer data, it can be interrupted at anytime.

%package devel
Summary:        http-parser devel
Group:          Development/Tools
Requires:       %{name} = %{version}
%description devel
This contains development tools and libraries for http-parser.

%prep
%setup -q
sed -i 's/ln -s \$(LIBDIR)\/\$(SONAME) \$(LIBDIR)\/libhttp_parser.\$(SOEXT)/pushd \$(LIBDIR) \&\& ln -s  \$(SONAME)  libhttp_parser.\$(SOEXT) \&\& popd/g' Makefile

%build
make PREFIX=%{_prefix} %{?_smp_mflags}

%install
make PREFIX="%{buildroot}%{_prefix}" DESTDIR="%{buildroot}" install

%files
%defattr(-,root,root)
%{_libdir}/libhttp_parser.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/http_parser.h
%{_libdir}/libhttp_parser.so

%changelog
*    Tue Jun 27 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.1-1
-    Initial version of http-parser package for Photon.
