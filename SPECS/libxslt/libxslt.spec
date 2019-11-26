Summary:        Libxslt-1.1.29
Name:           libxslt
Version:        1.1.32
Release:        2%{?dist}
License:        MIT
URL:            http:/http://xmlsoft.org/libxslt/
Group:          System Environment/General Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://xmlsoft.org/sources/%{name}-%{version}.tar.gz
%define sha1    libxslt=c47969f16747a72f9095b6a7a56d3afdd1e6e9ac
Requires:       libxml2-devel
BuildRequires:  libxml2-devel
%description
The libxslt package contains XSLT libraries used for extending libxml2 libraries to support XSLT files.

%package devel
Summary:        Development Libraries for libxslt
Group:          Development/Libraries
Requires:       libxslt = %{version}-%{release}
%description devel
Header files for doing development with libxslt.

%prep
%setup -q
%build
%configure \
    $(test %{_host} != %{_build} && echo "--with-sysroot=/target-%{_arch}") \
    --disable-static \
    --without-python
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%{_libdir}/*.sh
%{_libdir}/libxslt-plugins
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_includedir}/*
%{_docdir}/*
%{_datadir}/aclocal/*
%{_mandir}/man3/*

%changelog
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.32-2
-   Cross compilation support
*   Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 1.1.32-1
-   Update to version 1.1.32.
*   Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> 1.1.29-4
-   Applied patches for CVE-2015-9019 and CVE-2017-5029.
*   Tue May 23 2017 Kumar Kaushik <kaushikk@vmware.com> 1.1.29-3
-   Build does not requires python.
*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.29-2
-   Moved man3 to devel subpackage.
*   Fri Oct 21 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.1.29-1
-   Fix CVEs 2016-1683, 2016-1684, 2015-7995 with version 1.1.29
*   Mon Oct 03 2016 Chang Lee <changlee@vmware.com> 1.1.28-4
-   Modified check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1.28-3
-   GA - Bump release of all rpms
*   Tue Jan 19 2016 Xiaolin Li <xiaolinl@vmware.com> 1.1.28-2
-   Add a dev subpackage.
*   Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> 1.1.28-1
-   Initial build.  First version
