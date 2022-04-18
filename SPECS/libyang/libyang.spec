Summary:        YANG data modeling language library
Name:           libyang
Version:        2.0.164
Release:        1%{?dist}
Url:            https://github.com/CESNET/libyang
License:        BSD-3-Clause
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/CESNET/libyang/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha1 %{name}=2df5e4fa47c53b9d9d0477314664641f57e0025c

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pcre2-devel

%if 0%{with_check}
BuildRequires:   cmocka
BuildRequires:   valgrind
%endif

Requires:   pcre2

%description
Libyang is YANG data modeling language parser and toolkit
written (and providing API) in C.

%package devel
Summary:    Development files for libyang

%description devel
Files needed to develop with libyang.

%package tools
Summary:        YANG validator tools
Requires:       %{name} = %{version}-%{release}

%description tools
YANG validator tools.

%prep
%autosetup -p1

%build
mkdir build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
    -DCMAKE_BUILD_TYPE:String="Release" \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DENABLE_TESTS=ON \
    ..
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
%if 0%{?with_check}
cd build
make test %{?_smp_mflags}
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%license LICENSE
%{_libdir}/%{name}.so.2
%{_libdir}/%{name}.so.2.*
%exclude %dir %{_libdir}/debug

%files tools
%defattr(-, root, root)
%{_bindir}/yanglint
%{_bindir}/yangre
%{_datadir}/man/man1/yanglint.1.gz
%{_datadir}/man/man1/yangre.1.gz

%files devel
%defattr(-, root, root)
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/*.h

%changelog
* Fri Mar 25 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 2.0.164-1
- Modified from provided libyang.spec on GitHub. Needed for libnetconf2.