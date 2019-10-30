Summary:	Contains a utility for determining file types
Name:		file
Version:	5.24
Release:	4%{?dist}
License:	BSD
URL:		http://www.darwinsys.com/file
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
%define sha1 file=152daac79ccb4560dc65d5aaf754196ec1536f1d
Patch0:         0001-Avoid-reading-past-the-end-of-buffer-Rui-Reis.patch
Patch1:		CVE-2019-18218.patch
%description
The package contains a utility for determining the type of a
given file or files
%prep
%setup -q
%patch0 -p1
%patch1 -p1
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
