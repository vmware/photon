Summary:	PostgreSQL database engine
Name:		postgresql
Version:	9.5.0
Release:	1%{?dist}
License:	PostgreSQL
URL:		www.postgresql.org
Group:		Applications/Databases
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.postgresql.org/pub/source/v%{version}/%{name}-%{version}.tar.bz2
%define sha1 postgresql=930afeb713b81778f29d32e7bf18fd08ce2aa8f9
Requires:	openssl
Requires: 	python2
BuildRequires: 	perl
BuildRequires:	python2
BuildRequires:  openssl
BuildRequires:  krb5
BuildRequires:  openldap
BuildRequires:  libxml2
BuildRequires:  python2
BuildRequires:  libxslt
BuildRequires:  readline-devel

%description
PostgreSQL is an object-relational database management system. 

%prep
%setup -q
%build
sed -i '/DEFAULT_PGSOCKET_DIR/s@/tmp@/run/postgresql@' src/include/pg_config_manual.h &&
./configure \
	--prefix=%{_prefix} \
	--enable-thread-safety \
        --docdir=%{_docdir}/postgresql-%{version} 
make %{?_smp_mflags}
%install
cd src
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot} &&

%{_fixperms} %{buildroot}/*
%check
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%exclude %{_libdir}/debug/
%{_includedir}/*
%{_datadir}/postgresql/*
%changelog
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 9.5.0-1
-   Updated to version 9.5.0
*	Thu Aug 13 2015 Divya Thaluru <dthaluru@vmware.com> 9.4.4-1
-	Update to version 9.4.4.
*	Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> 9.4.1-2
-	Exclude /usr/lib/debug
*	Tue May 15 2015 Sharath George <sharathg@vmware.com> 9.4.1-1
-	Initial build.	First version
