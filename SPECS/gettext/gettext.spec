Summary:	Utilities for internationalization and localization
Name:		gettext
Version:	0.19.8
Release:	1%{?dist}
License:	GPLv3
URL:		http://www.gnu.org/software/gettext
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnu.org/gnu/gettext/%{name}-%{version}.tar.xz
%define sha1 gettext=dc551d4783edf691c1f0095ca927d3128b5093e8

%description
These allow programs to be compiled with NLS
(Native Language Support), enabling them to output
messages in the user's native language.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--docdir=%{_defaultdocdir}/%{name}-%{version} \
	--disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}/usr/share/doc/gettext-%{version}/examples
rm -rf %{buildroot}%{_infodir}
%find_lang %{name} --all-name

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/gettext/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/*.a
%{_datarootdir}/aclocal/*
%{_datarootdir}/%{name}-%{version}/*
%{_defaultdocdir}/%{name}-%{version}/*
%{_datarootdir}/%{name}/*
%{_mandir}/*

%changelog
*	Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 0.19.8-1
-	Upgrade to 0.19.8
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.19.5.1-2
-	GA - Bump release of all rpms
* 	Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 0.19.5.1-1
- 	Updated to version 0.19.5.1
*	Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 0.18.3.2-2
-	Handled locale files with macro find_lang
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 0.18.3.2-1
-	Initial build. First version
