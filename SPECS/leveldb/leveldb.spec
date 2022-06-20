Summary:	A fast and lightweight key/value database library by Google
Name:		leveldb
Version:	1.22
Release:	2%{?dist}
License:	BSD
URL:		https://github.com/google/leveldb
Group:		Development/Libraries/C and C++
Vendor:		VMware, Inc.
Distribution:	Photon

Source0:	https://github.com/google/leveldb/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=f9bbf5f466e7f707b94e19261762319ea9f65d41911690e84f59098551e2e69beccf756a414d705ade74ee96fd979bdb8b94c171c6f2cc83873cbd4a9380dbab

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
%make_install %{?_smp_mflags}
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cp -a %{name}.pc %{buildroot}%{_libdir}/pkgconfig/
rm -rf %{buildroot}/%{_libdir}/cmake

%if 0%{?with_check}
%check
ctest -V %{?_smp_mflags}
%endif

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
* Tue Jun 21 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.22-2
- Bump version as a part of sqlite upgrade
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
