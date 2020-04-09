Summary:	Contains a utility for determining file types
Name:		file
Version:	5.38
Release:	1%{?dist}
License:	BSD
URL:		http://www.darwinsys.com/file
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
%define sha1 file=57cad9341c3f74f8681c2ef931786c420105f35e
%description
The package contains a utility for determining the type of a
given file or files
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/*/*
%{_datarootdir}/misc/magic.mgc
%changelog
*	Wed Apr 08 2020 Siju Maliakkal <smaliakkal@vmware.com> 5.38-1
-	Upgrade to 5.38
-	CVE-2019-8904, CVE-2019-8905, CVE-2019-8906, CVE-2019-8907
*	Wed Oct 30 2019 Siju Maliakkal <smaliakkal@vmware.com> 5.24-4
-	Patch for CVE-2019-18218
*	Wed Aug 01 2018 Ankit Jain <ankitja@vmware.com> 5.24-3
-	Fix for CVE-2018-10360
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.24-2
-	GA - Bump release of all rpms
* 	Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 5.24-1
- 	Updated to version 5.24
*	Mon Apr 6 2015 Divya Thaluru <dthaluru@vmware.com> 5.22-1
-	Initial build. First version
