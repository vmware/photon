Summary:	A library that provides compression and decompression of file formats used by Microsoft
Name:		libmspack
Version:	0.7.1alpha
Release:	1%{?dist}
License:	LGPLv2+
URL:		http://www.cabextract.org.uk/libmspack/libmspack-0.5alpha.tar.gz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.cabextract.org.uk/libmspack/%{name}-%{version}.tar.gz
%define sha1 libmspack=073348180586d7b0f61fd7f971162ffb5c1f6621

%description
A library that provides compression and decompression of file formats used by Microsoft

%prep
%setup -q

%build
%configure
#libmspack does not support parallel make
make

%install
make DESTDIR=%{buildroot} install

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_bindir}/cabrip
%{_bindir}/chmextract
%{_bindir}/msexpand
%{_bindir}/oabextract

%changelog
* Fri Jul 26 2019 Sujay G <gsujay@vmware.com> 0.7.1alpha-1
- Bump version to 0.7.1alpha to fix CVE-2018-14681 & CVE-2018-14682
* Mon Nov 12 2018 Sujay G <gsujay@vmware.com> 0.5alpha-5
- Patch for CVE-2018-14679 & CVE-2018-14680
* Tue Jul 24 2018 Ajay Kaher <akaher@vmware.com> 0.5alpha-4
- Patch for CVE-2017-11423.patch
* Mon May 21 2018 Anish Swaminathan <anishs@vmware.com> 0.5alpha-3
- Patch for CVE-2017-6419
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.5alpha-2
- GA - Bump release of all rpms
* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 0.5-1
- Updated to version 0.5
* Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 0.4-1
- Initial version
