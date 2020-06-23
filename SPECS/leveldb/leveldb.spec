Summary:	A fast and lightweight key/value database library by Google
Name:		leveldb
Version:	1.22
Release:	1%{?dist}
License:	BSD
URL:		https://github.com/google/leveldb
Source0:	https://github.com/google/leveldb/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha1 leveldb=8d310af5cfb53dc836bfb412ff4b3c8aea578627
Group:		Development/Libraries/C and C++
Vendor:		VMware, Inc.
Distribution:	Photon

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  snappy-devel
BuildRequires:  sqlite-devel

%description
A fast and lightweight key/value database library.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
%description	devel
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

%files devel
%defattr(-,root,root)
%doc doc/
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
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
