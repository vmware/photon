Summary:	TIFF libraries and associated utilities.
Name:		libtiff
Version:	4.0.6
Release:	3%{?dist}
License:	libtiff
URL:		http://www.remotesensing.org/libtiff
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://download.osgeo.org/%{name}/tiff-%{version}.tar.gz
%define sha1 tiff=280e27704eaca5f592b82e71ac0c78b87395e2de
Patch0:		libtiff-4.0.6-CVE-2015-8668.patch
Patch1:		libtiff-4.0.6-CVE-2015-7554.patch
Patch2:		libtiff-4.0.6-CVE-2015-8683+CVE-2015-8665.patch
Patch3:     	libtiff-4.0.6-CVE-2016-3186.patch
Patch4:     	libtiff-4.0.6-CVE-2015-1547.patch
Patch5:     	libtiff-4.0.6-CVE-2016-3945.patch
Patch6:     	libtiff-4.0.6-CVE-2016-3990.patch
Patch7:     	libtiff-4.0.6-CVE-2016-3991.patch
BuildRequires:	libjpeg-turbo-devel
Requires:	libjpeg-turbo
%description
The LibTIFF package contains the TIFF libraries and associated utilities. The libraries are used by many programs for reading and writing TIFF files and the utilities are used for general work with TIFF files.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
%description	devel
It contains the libraries and header files to create applications 

%prep
%setup -q -n tiff-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p2
%patch6 -p2
%patch7 -p2

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
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*       Wed Oct 12 2016 Dheeraj Shetty <dheerajs@vmware.com> 4.0.6-3
-       Fixed security issues : CVE-2016-3945, CVE-2016-3990, CVE-2016-3991
*       Thu Sep 22 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.0.6-2
-       Fixed security issues : CVE-2015-8668, CVE-2015-7554, CVE-2015-8683+CVE-2015-8665,CVE-2016-3186
        CVE-2015-1547
*       Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 4.0.6-1
-       Initial version
