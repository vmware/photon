Summary:        A fast and lightweight key/value database library by Google
Name:           leveldb
Version:        1.23
Release:        1%{?dist}
License:        BSD
URL:            https://github.com/google/leveldb
Source0:        https://github.com/google/leveldb/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha1    leveldb=042e267eae6ab522fe29274f79ad45cde3977655
Group:          Development/Libraries/C and C++
Vendor:         VMware, Inc.
Distribution:   Photon
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
exec_prefix=${prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name: %{name}
Description: %{summary}
Version: %{version}
Libs: -l%{name}
EOF

# clone googletest and benchmark which are in .gitmodules
cd third_party/benchmark
git clone https://github.com/google/benchmark .
cd ../googletest/
git clone https://github.com/google/googletest.git .

%build
%cmake .
%make_build

%install
%make_install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -a %{name}.pc %{buildroot}%{_libdir}/pkgconfig/
rm -rf %{buildroot}/%{_libdir}/cmake

%check
ctest -V %{?_smp_mflags}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/lib%{name}.so.*
%{_libdir}/libbenchmark.so.*
%{_libdir}/libgmock.so.*
%{_libdir}/libgmock_main.so.*
%{_libdir}/libbenchmark_main.so.*
%{_libdir}/libgtest.so.*
%{_libdir}/libgtest_main.so.*

%files devel
%defattr(-,root,root)
%doc doc/
%{_includedir}/%{name}/
%{_includedir}/benchmark/
%{_includedir}/gmock/
%{_includedir}/gtest/
%{_libdir}/lib%{name}.so
%{_libdir}/libbenchmark.so
%{_libdir}/libgmock.so
%{_libdir}/libgmock_main.so
%{_libdir}/libbenchmark_main.so
%{_libdir}/libgtest.so
%{_libdir}/libgtest_main.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.23-1
-   Automatic Version Bump
*   Wed Jul 29 2020 Shreenidhi Shedi <sshedi@vmware.com> 1.22-1
-   Upgrade to version 1.22
*   Tue Apr 25 2017 Divya Thaluru <dthaluru@vmware.com> 1.20-2
-   Added pkgconfig file for leveldb
*   Thu Mar 30 2017 Divya Thaluru <dthaluru@vmware.com> 1.20-1
-   Updated to version 1.20
*   Wed Dec 21 2016 Dheeraj Shetty <Dheerajs@vmware.com> 1.19-2
-   Fixed parallel build error
*   Fri Dec 16 2016 Dheeraj Shetty <Dheerajs@vmware.com> 1.19-1
-   Initial build. First version
