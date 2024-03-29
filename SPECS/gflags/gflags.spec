Summary:        Library for commandline flag processing
Name:           gflags
Version:        2.2.2
Release:        1%{?dist}
License:        MIT
Group:          Development/Libraries/C++
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://gflags.github.io/gflags

Source0: https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=98c4703aab24e81fe551f7831ab797fb73d0f7dfc516addb34b9ff6d0914e5fd398207889b1ae555bac039537b1d4677067dae403b64903577078d99c1bdb447

BuildRequires:  cmake
BuildRequires:  gcc

%description
The gflags package contains a C++ library that implements
commandline flags processing. It includes built-in support
for standard types such as string and the ability to define
flags in the source file in which they are used.

%package devel
Summary:    Development files for %{name}
Group:      Development/Libraries/C++
Requires:   %{name} = %{version}-%{release}

%description devel
Development files for %{name} library.

%prep
%autosetup -p1

%build
%cmake -DBUILD_TESTING:BOOL=ON \
       -DINSTALL_HEADERS:BOOL=ON \
       -DREGISTER_BUILD_DIR:BOOL=OFF \
       -DREGISTER_INSTALL_PREFIX:BOOL=OFF

%cmake_build

%install
%cmake_install

%if 0%{?with_check}
%check
%ctest
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING.txt
%doc AUTHORS.txt ChangeLog.txt README.md
%{_bindir}/gflags_completions.sh
%{_libdir}/libgflags.so.*
%{_libdir}/libgflags_nothreads.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/
%{_libdir}/libgflags.so
%{_libdir}/libgflags_nothreads.so
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Mon Apr 04 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.2.2-1
- gflags initial build
