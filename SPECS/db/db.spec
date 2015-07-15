Summary:	DB-5.3.28
Name:		db
Version:	5.3.28
Release:	1%{?dist}
License:	Sleepycat License
URL:		https://oss.oracle.com/berkeley-db.html
Source0:	http://download.oracle.com/berkeley-db/%{name}-%{version}.tar.gz
%define sha1 db=fa3f8a41ad5101f43d08bc0efb6241c9b6fc1ae9
Group:		Databases
Vendor:		VMware, Inc.
Distribution:	Photon
%description
The Berkeley DB package contains programs and utilities used by many other applications for database related functions.

%package docs
Summary: DB docs
Group: Databases
%description docs
The package contains the DB doc files

%prep
%setup -q
%build
cd build_unix
../dist/configure \
	--prefix=%{_prefix} \
	--enable-compat185 \
	--enable-dbm       \
	--disable-static   \
	--enable-cxx
make %{?_smp_mflags}
%install
pushd build_unix
make DESTDIR=%{buildroot} docdir=%{_docdir}/%{name}-%{version} install
popd
find %{buildroot} -name '*.la' -delete
%clean
rm -rf %{buildroot}
%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so
%{_includedir}/*

%files docs
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}/*

%changelog
*	Sun Jan 04 2015 Touseef Liaqat <tliaqat@vmware.com> 6.1.19-1
-	Created separated docs package. First version
*	Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 6.1.19-1
-	Initial build. First version
