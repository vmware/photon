%define re2_long_ver 2022-06-01

Name:           re2
Version:        20220601
Release:        1%{?dist}
Summary:        Google RPC
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        BSD
URL:            http://github.com/google/%{name}

Source0:        https://github.com/google/re2/archive/%{name}-%{re2_long_ver}.tar.gz
%define sha512  %{name}=f3d5f2a3aa5eda74bc8f434d7b000eed8e107c894307a889466a4cb16a15b352a0332e10d80ed603c9e2e38bbcbdf11f15b6953cbdf461cc9fb0560e89a8ceb8

BuildRequires: cmake

%description
RE2 is a C++ library providing a fast, safe, thread-friendly alternative to
backtracking regular expression engines like those used in PCRE, Perl, and
Python.

Backtracking engines are typically full of features and convenient syntactic
sugar but can be forced into taking exponential amounts of time on even small
inputs.

In contrast, RE2 uses automata theory to guarantee that regular expression
searches run in time linear in the size of the input, at the expense of some
missing features (e.g back references and generalized assertions).

%package        devel
Summary:        C++ header files and library symbolic links for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains the C++ header files and symbolic links to the shared
libraries for %{name}. If you would like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%autosetup -p1 -n %{name}-%{re2_long_ver}

%build
%cmake . \
    -DOVERRIDE_INSTALL_PREFIX=/usr \
    -DCMAKE_COLOR_MAKEFILE:BOOL=OFF \
    -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
    "-GUnix Makefiles"

%cmake_build

%install
%cmake_install

# Suppress the static library
rm -fv %{buildroot}%{_libdir}/libre2.a

mkdir -p %{buildroot}%{_libdir}/pkgconfig/

# This gets done in Makefile, but nothing in CMake build does it:
# https://github.com/google/re2/issues/349
sed -i -e 's,@includedir@,%{_includedir},g' re2.pc
sed -i -e 's,@libdir@,%{_libdir},g' re2.pc
install -m 0644 re2.pc %{buildroot}%{_libdir}/pkgconfig/

%check
%make_build test

%ldconfig_scriptlets

%files
%license LICENSE
%doc AUTHORS CONTRIBUTORS README
%{_libdir}/libre2.so.9*

%files devel
%{_includedir}/re2/
%{_libdir}/libre2.so
%{_libdir}/pkgconfig/re2.pc
%{_libdir}/cmake/re2/*.cmake

%changelog
* Tue Nov 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 20220601-1
- Initial Build
