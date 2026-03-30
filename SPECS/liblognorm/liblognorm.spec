%global build_if %{photon_subrelease} >= 92

Name:           liblognorm
Version:        2.0.9
Release:        1%{?dist}
Summary:        Fast samples-based log normalization library
URL:            http://www.liblognorm.com
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/rsyslog/liblognorm/archive/refs/tags/%{name}-%{version}.tar.gz
Source1: license.txt
%include %{SOURCE1}

BuildRequires:  gcc
BuildRequires:  chrpath
BuildRequires:  libfastjson-devel
BuildRequires:  libestr-devel
BuildRequires:  pcre2-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  libltdl-devel

Requires:  %{name}-libs = %{version}-%{release}

%description
Briefly described, liblognorm is a tool to normalize log data.

People who need to take a look at logs often have a common problem. Logs from
different machines (from different vendors) usually have different formats for
their logs. Even if it is the same type of log (e.g. from firewalls), the log
entries are so different, that it is pretty hard to read these. This is where
liblognorm comes into the game. With this tool you can normalize all your logs.
All you need is liblognorm and its dependencies and a sample database that fits
the logs you want to normalize.

%package libs
Summary: libs for programs using liblognorm library

Requires:  chrpath
Requires:  libfastjson
Requires:  libestr
Requires:  pcre2
Requires:  libtool
Requires:  libltdl

%description libs
The liblognorm-libs package includes libraries necessary for programs which use liblognorm library.

%package devel
Summary:        Development tools for programs using liblognorm library
Requires:       %{name} = %{version}-%{release}
Requires:       json-c-devel
Requires:       libestr-devel

%description devel
The liblognorm-devel package includes header files, libraries necessary for
developing programs which use liblognorm library.

%prep
%autosetup -p1

%build
autoreconf -vfi
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install

%post libs
/sbin/ldconfig

%postun libs
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/lognormalizer

%files libs
%defattr(-,root,root)
%{_libdir}/liblognorm.so.5
%{_libdir}/liblognorm.so.5.1.0

%files devel
%defattr(-,root,root)
%{_includedir}/annot.h
%{_includedir}/enc.h
%{_includedir}/liblognorm.h
%{_includedir}/lognorm-features.h
%{_includedir}/lognorm.h
%{_includedir}/parser.h
%{_includedir}/pdag.h
%{_includedir}/samp.h
%{_libdir}/liblognorm.so
%{_libdir}/pkgconfig/lognorm.pc

%changelog
* Fri Mar 13 2026 Tapas Kundu <tapas.kundu@broadcom.com> 2.0.9-1
- Initial version
