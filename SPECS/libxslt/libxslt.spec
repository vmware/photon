Summary:        Libxslt-1.1.29
Name:           libxslt
Version:        1.1.32
Release:        8%{?dist}
License:        MIT
URL:            http:/http://xmlsoft.org/libxslt/
Group:          System Environment/General Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://xmlsoft.org/sources/%{name}-%{version}.tar.gz
%define sha1    libxslt=c47969f16747a72f9095b6a7a56d3afdd1e6e9ac
Patch0:         libxslt-CVE-2019-11068.patch
Patch1:         libxslt-CVE-2019-13117.patch
Patch2:         libxslt-CVE-2019-13118.patch
Patch3:         CVE-2019-18197.patch
Patch4:         libxslt-CVE-2019-5815.patch
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
%autosetup -p1
sed -i 's/int xsltMaxDepth = 3000/int xsltMaxDepth = 5000/g' libxslt/transform.c

%build
sh configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --disable-static \
    --without-python
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install %{?_smp_mflags}
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
*   Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 1.1.32-8
-   Version bump up to use libxml2 2.9.11-4.
*   Fri Mar 13 2020 Shreyas B. <shreyasb@vmware.com> 1.1.32-7
-   Increase the maximum number of nested template calls for xml.
*   Tue Dec 17 2019 Shreyas B. <shreyasb@vmware.com> 1.1.32-6
-   Apply patch for CVE-2019-5815: READ heap-buffer-overflow in libxslt.
*   Tue Oct 29 2019 Siju Maliakkal <smaliakkal@vmware.com> 1.1.32-5
-   Apply patch for CVE-2019-18197
*   Mon Jul 22 2019 Shreyas B. <shreyasb@vmware.com> 1.1.32-4
-   Apply patch for CVE-2019-13118
*   Thu Jul 18 2019 Shreyas Behera <shreyasb@vmware.com> 1.1.32-3
-   Apply patch for CVE-2019-13117
*   Fri Apr 12 2019 Siju Maliakkal <smaliakkal@vmware.com> 1.1.32-2
-   Applied patch for CVE-2019-11068
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
