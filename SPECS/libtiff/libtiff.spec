Summary:	TIFF libraries and associated utilities.
Name:		libtiff
Version:	4.0.7
Release:	1%{?dist}
License:	libtiff
URL:		http://www.remotesensing.org/libtiff
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://download.osgeo.org/%{name}/tiff-%{version}.tar.gz
%define sha1 tiff=2c1b64478e88f93522a42dd5271214a0e5eae648
Patch0:		libtiff-4.0.6-CVE-2015-7554.patch
Patch1:     	libtiff-4.0.6-CVE-2015-1547.patch
BuildRequires:	libjpeg-turbo-devel
Requires:	libjpeg-turbo
%description
The LibTIFF package contains the TIFF libraries and associated utilities. The libraries are used by many programs for reading and writing TIFF files and the utilities are used for general work with TIFF files.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
Requires:	libjpeg-turbo-devel
%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q -n tiff-%{version}
%patch0 -p1
%patch1 -p1

%build
./configure \
	--prefix=%{_prefix} \
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
