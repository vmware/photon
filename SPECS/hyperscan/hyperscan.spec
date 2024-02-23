Name:           hyperscan
Version:        5.4.0
Release:        4%{?dist}
Summary:        High-performance regular expression matching library
License:        BSD
URL:            https://www.hyperscan.io
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/intel/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%define sha512 hyperscan=cfec3f43b9e8b3fbb2e761927f3a173c1230f2688da710ec7708f2941ce6f550a1d3cb48b0b0e2ccf709807390117a7e40047cb99190bcc341f37eb3da13ae62

BuildRequires:  gcc
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  pcre-devel
BuildRequires:  python3-devel
BuildRequires:  sqlite-devel >= 3.0
BuildRequires:  libpcap-devel
BuildRequires:  ragel
BuildRequires:  colm-devel

#package requires SSE support and fails to build on non x86_64 archs
BuildArch:      x86_64

%description
Hyperscan is a high-performance multiple regex matching library. It
follows the regular expression syntax of the commonly-used libpcre
library, but is a standalone library with its own C API.

Hyperscan uses hybrid automata techniques to allow simultaneous
matching of large numbers (up to tens of thousands) of regular
expressions and for the matching of regular expressions across streams
of data.

Hyperscan is typically used in a DPI library stack.

%package devel
Summary: Libraries and header files for the hyperscan library
Requires: %{name} = %{version}-%{release}

%description devel
Hyperscan is a high-performance multiple regex matching library. It
follows the regular expression syntax of the commonly-used libpcre
library, but is a standalone library with its own C API.

Hyperscan uses hybrid automata techniques to allow simultaneous
matching of large numbers (up to tens of thousands) of regular
expressions and for the matching of regular expressions across streams
of data.

Hyperscan is typically used in a DPI library stack.

This package provides the libraries, include files and other resources
needed for developing Hyperscan applications.

%prep
%autosetup -p1

%build
# https://github.com/intel/hyperscan/issues/292#issuecomment-762635447
sed -i -e 's|\[^ \]|\[^ @\]|g' "cmake/build_wrapper.sh"

# LTO seems to be losing the target prefix on ifunc targets leading to
# multiply defined symbols.  This seems like a GCC bug
# Disable LTO
%define _lto_cflags %{nil}
mkdir build
cmake \
    -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir} \
    -DCMAKE_INSTALL_DOCDIR:PATH=%{_docdir} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DBUILD_STATIC_AND_SHARED:BOOL=OFF .
%make_build

%install
%make_install

%ldconfig_scriptlets

%if 0%{?with_check}
%check
./bin/unit-hyperscan
%endif

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license COPYING
%license LICENSE
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/libhs.pc
%{_includedir}/hs/*
%doc %{_docdir}/examples/README.md
%doc %{_docdir}/examples/*.cc
%doc %{_docdir}/examples/*.c

%changelog
* Fri Feb 23 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 5.4.0-4
- Bump version as a part of sqlite upgrade to v3.43.2
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 5.4.0-3
- bump release as part of sqlite update
* Thu Oct 20 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 5.4.0-2
- Fix build with latest toolchain
* Thu Jul 28 2022 Mukul Sikka <msikka@vmware.com> 5.4.0-1
- Initial Build
