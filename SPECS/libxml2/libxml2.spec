Summary:	Libxml2
Name:		libxml2
Version:	2.9.4
Release:	2%{?dist}
License:	MIT
URL:		http://xmlsoft.org/
Group:		System Environment/General Libraries
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	ftp://xmlsoft.org/libxml2/%{name}-%{version}.tar.gz
Patch0:         libxml2-2.9.4-support-cve-2016-5131.patch
Patch1:         libxml2-2.9.4-cve-2016-5131.patch
%define sha1 libxml2=958ae70baf186263a4bd801a81dd5d682aedd1db
Requires:	python2
BuildRequires:	python2-devel
BuildRequires:	python2-libs
Provides:	pkgconfig(libxml-2.0)

%description
The libxml2 package contains libraries and utilities used for parsing XML files. 

%package python
Summary:    The libxml2 python module
Group:      Development/Languages/Python
Requires:   %{name} = %{version}
Requires:   python2
Requires:   python2-libs

%description python
The libxml2 python module


%package devel
Summary:    Libraries and header files for libxml
Requires:	%{name} = %{version}

%description devel
Static libraries and header files for the support library for libxml

%prep
%setup -q
%patch0 -p1
%patch1 -p1
sed \
  -e /xmlInitializeCatalog/d \
  -e 's/((ent->checked =.*&&/(((ent->checked == 0) ||\
          ((ent->children == NULL) \&\& (ctxt->options \& XML_PARSE_NOENT))) \&\&/' \
  -i parser.c
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--disable-static \
	--with-history
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot}/%{_libdir} -name '*.la' -delete
%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_docdir}/*
%{_libdir}/libxml*
%{_libdir}/xml2Conf.sh
%{_bindir}/*
%{_datadir}/aclocal/*
%{_datadir}/gtk-doc/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%files python
%defattr(-,root,root)
%{_libdir}/python*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/libxml-2.0.pc
%{_libdir}/cmake/libxml2/libxml2-config.cmake


%changelog
*	Thu Oct 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.4-2
-	Apply patch for CVE-2016-5131
*       Wed Jun 01 2016 Anish Swaminathan <anishs@vmware.com> 2.9.4-1
-       Upgrade to 2.9.4
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.3-2
-	GA - Bump release of all rpms
*       Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.9.3-1
-       Upgraded to version 2.9.3
*       Thu Jan 28 2016 Xiaolin Li <xiaolinl@vmware.com> 2.9.2-1
-       Downgrade to version 2.9.2
-       libxml 2.9.3 has been found to have major functional issues. 
-       Until these are resolved, please roadmap updating to 2.9.2.
*       Wed Dec 2 2015 Xiaolin Li <xiaolinl@vmware.com> 2.9.3-1
-       Update to version 2.9.3
*       Thu Jul 2 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.9.1-3
-       Seperate the python module from the main library
*	Thu Jun 11 2015 Alexey Makhalov <amakhalov@vmware.com> 2.9.1-2
-	Moved 'Provides: pkgconfig(...)' into base package
*	Mon Oct 13 2014 Divya Thaluru <dthaluru@vmware.com> 2.9.1-1
-	Initial build.	First version
