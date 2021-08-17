Summary:        A fast and lightweight key/value database library by Google
Name:           leveldb
Version:        1.23
Release:        2%{?dist}
License:        BSD
URL:            https://github.com/google/leveldb
Group:          Development/Libraries/C and C++
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/google/leveldb/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha1    %{name}=042e267eae6ab522fe29274f79ad45cde3977655

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

%build
%cmake -DLEVELDB_BUILD_TESTS:BOOL=OFF \
       -DLEVELDB_BUILD_BENCHMARKS:BOOL=OFF
%make_build

%install
%make_install

mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -a %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

%check
ctest -V %{?_smp_mflags}

%ldconfig_scriptlets

%files
%license LICENSE
%doc AUTHORS README.md NEWS
%{_libdir}/lib%{name}.so.*

%files devel
%doc doc/ CONTRIBUTING.md TODO
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/

%changelog
*   Wed Aug 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.23-2
-   Remove test suite and benchmark related files
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
