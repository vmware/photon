Summary:        Compression and decompression routines
Name:           zlib
Version:        1.2.11
Release:        3%{?dist}
URL:            http://www.zlib.net/
License:        zlib
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.zlib.net/%{name}-%{version}.tar.xz
%define sha1    zlib=e1cb0d5c92da8e9a8c2635dfa249c341dfd00322
%description
Compression and decompression routines
%package    devel
Summary:    Header and development files for zlib
Requires:   %{name} = %{version}
%description    devel
It contains the libraries and header files to create applications 
for handling compiled objects.
%prep
%setup -q
%build
if [ %{_host} != %{_build} ]; then
export CC=%{_host}-gcc
export CXX=%{_host}-g++
export AR=%{_host}-ar
export AS=%{_host}-as
export RANLIB=%{_host}-ranlib
export LD=%{_host}-ld
export STRIP=%{_host}-strip
fi
sh configure --prefix=%{_prefix} --shared
make V=1 %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}/%{_lib}
ln -sfv ../../lib/$(readlink %{buildroot}%{_libdir}/libz.so) %{buildroot}%{_libdir}/libz.so

%check
make  %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_libdir}/libz.so*

%files devel
%{_includedir}/zconf.h
%{_includedir}/zlib.h
%{_libdir}/pkgconfig/zlib.pc
%{_libdir}/libz.a
%{_libdir}/libz.so
%{_mandir}/man3/zlib.3.gz

%changelog
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.11-3
-   Cross compilation support
*   Tue Nov 06 2018 Sriram Nambakam <snambakam@vmware.com> 1.2.11-2
-   Cross compilation support
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.11-1
-   Updated to version 1.2.11.
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.2.8-5
-   Moved man3 to devel subpackage.
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.2.8-4
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.8-3
-   GA - Bump release of all rpms
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> 1.2.8-2
-   Update according to UsrMove.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.2.8-1
-   Initial build. First version
