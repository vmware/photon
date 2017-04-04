Summary:	A utility for generating programs that recognize patterns in text
Name:		flex
Version:	2.6.0
Release:	1%{?dist}
License:	BSD
URL:		http://flex.sourceforge.net
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://prdownloads.sourceforge.net/flex/%{name}-%{version}.tar.gz
%define sha1 flex=cfe10b5de4893ced356adc437e78018e715818c3
BuildRequires:	m4
Requires:	m4
%description
The Flex package contains a utility for generating programs
that recognize patterns in text.

%package devel
Summary: Development libraries and header files for the flex library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The flex-devel package contains the development libraries and header files for
flex.

%prep
%setup -q
sed -i -e '/test-bison/d' tests/Makefile.in
%build
./configure \
	--prefix=%{_prefix} \
	--docdir=%{_defaultdocdir}/%{name}-%{version} \
	--disable-silent-rules
make VERBOSE=1 %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
cat > %{buildroot}/usr/bin/lex <<- "EOF"
#!/bin/sh
# Begin /usr/bin/lex

	exec /usr/bin/flex -l "$@"

# End /usr/bin/lex
EOF
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/flex
%{_bindir}/flex++
%attr(755,root,root) %{_bindir}/lex
%{_libdir}/*.so.*
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*

%changelog
*   Tue Apr 04 2017 Chang Lee <changlee@vmware.com> 2.6.0-1
-   Updated to version 2.6.0
*       Thu Oct 13 2016 Kumar Kaushik <kaushikk@vmware.com> 2.5.39-3
-       Fixing Security bug CVE-2016-6354.
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.5.39-2
-	GA - Bump release of all rpms
* 	Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 2.5.39-1
- 	Updated to version 2.5.39
*       Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 2.5.38-3
-       Moving static lib files to devel package.
*	Fri Jun 5 2015 Divya Thaluru <dthaluru@vmware.com> 2.5.38-2
-	Adding m4 package to build and run time required package 
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.5.38-1
-	Initial build.	First version
