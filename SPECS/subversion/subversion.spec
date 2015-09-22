Summary:    	The Apache Subversion control system
Name:       	subversion
Version:    	1.8.13
Release:    	4%{?dist}
License:    	Apache License 2.0
URL:        	http://subversion.apache.org/
Group:      	Utilities/System
Vendor:     	VMware, Inc.
Distribution: 	Photon
Source0:        http://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.gz
%define sha1 subversion=437cf662b7ed27d2254aa7ca334fdd74b49262ef
Requires:   	apr
Requires:   	apr-util
BuildRequires: 	apr-devel
BuildRequires: 	apr-util
BuildRequires: 	apr-util-devel
BuildRequires: 	sqlite-autoconf
BuildRequires: 	libtool
BuildRequires: 	expat

%description
The Apache version control system.

%package	devel
Summary:	Header and development files for mesos
Requires:	%{name} = %{version}
%description    devel
 subversion-devel package contains header files, libraries.

%prep
%setup -q
%build
./configure --prefix=%{_prefix}                        	\
	    --disable-static				\
	    --with-apache-libexecdir 

make %{?_smp_mflags}

%install
make -j1 DESTDIR=%{buildroot} install 

%files
%defattr(-,root,root)
%{_bindir}/svn*
%{_libdir}/libsvn_*.so.*
%{_mandir}/*
%lang(de) %{_datadir}/locale/de/LC_MESSAGES/subversion.mo
%lang(es) %{_datadir}/locale/es/LC_MESSAGES/subversion.mo
%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/subversion.mo
%lang(it) %{_datadir}/locale/it/LC_MESSAGES/subversion.mo
%lang(ja) %{_datadir}/locale/ja/LC_MESSAGES/subversion.mo
%lang(ko) %{_datadir}/locale/ko/LC_MESSAGES/subversion.mo
%lang(nb) %{_datadir}/locale/nb/LC_MESSAGES/subversion.mo
%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/subversion.mo
%lang(pt_BR) %{_datadir}/locale/pt_BR/LC_MESSAGES/subversion.mo
%lang(sv) %{_datadir}/locale/sv/LC_MESSAGES/subversion.mo
%lang(zh_CN) %{_datadir}/locale/zh_CN/LC_MESSAGES/subversion.mo
%lang(zh_TW) %{_datadir}/locale/zh_TW/LC_MESSAGES/subversion.mo

%files devel
%{_includedir}/*
%{_libdir}/libsvn_*.*a
%{_libdir}/libsvn_*.so
%exclude %{_libdir}/debug/

%changelog
* 	Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.13-4
-	Updated build-requires after creating devel package for apr. 
*   Mon Sep 21 2015 Xiaolin Li <xiaolinl@vmware.com> 1.8.13-3
-   Move .a, and .so files to devel pkg.
*	Tue Sep 08 2015 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.13-2
-	Move headers into devel pkg.
*	Fri Jun 26 2015 Sarah Choi <sarahc@vmware.com> 1.8.13-1
-	Initial build. First version
