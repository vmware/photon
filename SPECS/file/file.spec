Summary:	Contains a utility for determining file types
Name:		file
Version:	5.25
Release:	1%{?dist}
License:	BSD
URL:		http://www.darwinsys.com/file
Group:		Applications/File
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	ftp://ftp.astron.com/pub/file/%{name}-%{version}.tar.gz
%define sha1 file=fea78106dd0b7a09a61714cdbe545135563e84bd
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
*	Tue May 24 2016 Divya Thaluru <dthaluru@vmware.com> 5.25-1
- 	Updated to version 5.25
* 	Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 5.24-1
- 	Updated to version 5.24
*	Mon Apr 6 2015 Divya Thaluru <dthaluru@vmware.com> 5.22-1
-	Initial build. First version
