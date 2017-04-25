Summary:	A fast and lightweight key/value database library by Google
Name:		leveldb
Version:	1.20
Release:	2%{?dist}
License:	BSD
URL:		https://github.com/google/leveldb
Source0:	https://github.com/google/leveldb/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha1 leveldb=df11440c30deed5987263730180225db98de9f57
Group:		Development/Libraries/C and C++
Vendor:		VMware, Inc.
Distribution:	Photon

%description
leveldb implements a system for maintaining a persistent key/value store.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	devel
leveldb implements a system for maintaining a persistent key/value store.

%prep
%setup -q

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
make

%install
mkdir -p %{buildroot}{%{_libdir}/pkgconfig,%{_includedir}}
cp -a out-shared/lib%{name}.so* %{buildroot}%{_libdir}/
cp -a out-static/lib%{name}.a %{buildroot}%{_libdir}/
cp -a include/%{name}/ %{buildroot}%{_includedir}/
cp -a %{name}.pc %{buildroot}%{_libdir}/pkgconfig/

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/leveldb/
%{_libdir}/libleveldb.so
%{_libdir}/libleveldb.a
%{_libdir}/pkgconfig/%{name}.pc

%changelog
*	Tue Apr 25 2017 Divya Thaluru <dthaluru@vmware.com> 1.20-2
-	Added pkgconfig file for leveldb
*	Thu Mar 30 2017 Divya Thaluru <dthaluru@vmware.com> 1.20-1
-	Updated to version 1.20
*	Wed Dec 21 2016 Dheeraj Shetty <Dheerajs@vmware.com> 1.19-2
-	Fixed parallel build error
*	Fri Dec 16 2016 Dheeraj Shetty <Dheerajs@vmware.com> 1.19-1
-	Initial build. First version
