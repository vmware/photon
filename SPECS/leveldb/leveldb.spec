Summary:        A fast and lightweight key/value database library by Google
Name:           leveldb
Version:        1.23
Release:        6%{?dist}
License:        BSD
URL:            https://github.com/google/leveldb
Group:          Development/Libraries/C and C++
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/google/leveldb/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=ac15eac29387b9f702a901b6567d47a9f8c17cf5c7d8700a77ec771da25158c83b04959c33f3d4de7a3f033ef08f545d14ba823a8d527e21889c4b78065b0f84

BuildRequires:  git
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  snappy-devel
BuildRequires:  sqlite-devel

%description
A fast and lightweight key/value database library.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
%description    devel
%{summary}.

%prep
%autosetup -p1

cat > %{name}.pc << EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: %{name}
Description: %{summary}
Version: %{version}
Libs: -l%{name}
EOF

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Debug \
    -DLEVELDB_BUILD_TESTS:BOOL=OFF \
    -DLEVELDB_BUILD_BENCHMARKS:BOOL=OFF \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \

%cmake_build

%install
%cmake_install

mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -a %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

%if 0%{?with_check}
%check
ctest -V %{?_smp_mflags}
%endif

%ldconfig_scriptlets

%files
%license LICENSE
%doc AUTHORS README.md NEWS
%{_libdir}/lib%{name}.so.*

%files devel
%doc doc/ CONTRIBUTING.md TODO
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}

%changelog
* Mon Mar 04 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.23-6
- Bump version as a part of sqlite upgrade to v3.43.2
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 1.23-5
- bump release as part of sqlite update
* Sat Jul 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.23-4
- Bump version as a part of sqlite upgrade
* Fri Jun 17 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.23-3
- Fix build with latest cmake
* Wed Aug 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.23-2
- Remove test suite and benchmark related files
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.23-1
- Automatic Version Bump
* Wed Jul 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.22-1
- Upgrade to version 1.22
* Tue Apr 25 2017 Divya Thaluru <dthaluru@vmware.com> 1.20-2
- Added pkgconfig file for leveldb
* Thu Mar 30 2017 Divya Thaluru <dthaluru@vmware.com> 1.20-1
- Updated to version 1.20
* Wed Dec 21 2016 Dheeraj Shetty <Dheerajs@vmware.com> 1.19-2
- Fixed parallel build error
* Fri Dec 16 2016 Dheeraj Shetty <Dheerajs@vmware.com> 1.19-1
- Initial build. First version
