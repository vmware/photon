Summary:        Library for commandline flag processing
Name:           gflags
Version:        2.2.2
Release:        2%{?dist}
Group:          Development/Libraries/C++
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://gflags.github.io/gflags

Source0: https://github.com/%{name}/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 2.2.2-2
- Release bump for SRP compliance
* Mon Apr 04 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.2.2-1
- gflags initial build
