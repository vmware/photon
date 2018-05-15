Summary:        TIFF libraries and associated utilities.
Name:           libtiff
Version:        4.0.9
Release:        4%{?dist}
License:        libtiff
URL:            http://www.simplesystems.org/libtiff/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://download.osgeo.org/%{name}/tiff-%{version}.tar.gz
%define sha1    tiff=87d4543579176cc568668617c22baceccd568296
Patch0:         libtiff-4.0.9-CVE-2017-18013.patch
Patch1:         libtiff-4.0.9-CVE-2017-9935.patch
Patch2:         libtiff-4.0.9-CVE-2017-17095.patch
Patch3:         libtiff-4.0.9-CVE-2018-5784.patch
Patch4:         libtiff-4.0-9-CVE-2017-11613-1.patch
Patch5:         libtiff-4.0-9-CVE-2017-11613-2.patch
Patch6:         libtiff-4.0-9-CVE-2018-7456.patch
Patch7:         libtiff-4.0.9-CVE-2018-8905.patch
BuildRequires:  libjpeg-turbo-devel
Requires:       libjpeg-turbo
%description
The LibTIFF package contains the TIFF libraries and associated utilities. The libraries are used by many programs for reading and writing TIFF files and the utilities are used for general work with TIFF files.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libjpeg-turbo-devel
%description    devel
It contains the libraries and header files to create applications

%prep
%setup -q -n tiff-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%build
%configure \
    --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
make %{?_smp_mflags} -k check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/man/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/doc/*
%{_datadir}/man/man3/*

%changelog
*   Mon May 14 2018 Xiaolin Li <xiaolinl@vmware.com> 4.0.9-4
-   Fix CVE-2018-7456, CVE-2018-8905, CVE-2018-5784, CVE-2017-11613
*   Wed Feb 14 2018 Dheeraj Shetty <dheerajs@vmware.com> 4.0.9-3
-   Patch for CVE-2017-17095
*   Wed Jan 31 2018 Dheeraj Shetty <dheerajs@vmware.com> 4.0.9-2
-   Repatched CVE-2017-9935
*   Wed Jan 17 2018 Dheeraj Shetty <dheerajs@vmware.com> 4.0.9-1
-   Updated to version 4.0.9 to fix CVE-2017-11613, CVE-2017-9937,
-   CVE-2017-17973. Added a patch for CVE-2017-18013
*   Mon Dec 11 2017 Xiaolin Li <xiaolinl@vmware.com> 4.0.8-7
-   Added patch for CVE-2017-9935
*   Mon Nov 27 2017 Xiaolin Li <xiaolinl@vmware.com> 4.0.8-6
-   Added patches for CVE-2017-13726, CVE-2017-13727
*   Mon Nov 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.0.8-5
-   Patch : CVE-2017-12944
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 4.0.8-4
-   Use standard configure macros
*   Wed Aug 09 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.8-3
-   Added patch for CVE-2017-9936, CVE-2017-11335
*   Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> 4.0.8-2
-   Applied patch for CVE-2017-10688
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 4.0.8-1
-   Updated to version 4.0.8.
*   Tue May 16 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.7-4
-   Added patch for CVE-2016-10266, CVE-2016-10268, CVE-2016-10269, CVE-2016-10267 and libtiff-heap-buffer-overflow patch
*   Mon Apr 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.0.7-3
-   Patch : CVE-2016-10092, CVE-2016-10093, CVE-2016-10094
*   Thu Jan 19 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.0.7-2
-   Patch : CVE-2017-5225
*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 4.0.7-1
-   Update to 4.0.7. It fixes CVE-2016-953[3456789] and CVE-2016-9540
-   Remove obsolete patches
*   Wed Oct 12 2016 Dheeraj Shetty <dheerajs@vmware.com> 4.0.6-3
-   Fixed security issues : CVE-2016-3945, CVE-2016-3990, CVE-2016-3991
*   Thu Sep 22 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.6-2
-   Fixed security issues : CVE-2015-8668, CVE-2015-7554, CVE-2015-8683+CVE-2015-8665,CVE-2016-3186
-   CVE-2015-1547
*   Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 4.0.6-1
-   Initial version
