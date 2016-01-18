Summary:	DB-6.1.26
Name:		db
Version:	6.1.26
Release:	1%{?dist}
License:	Sleepycat License
URL:		https://oss.oracle.com/berkeley-db.html
Source0:	http://download.oracle.com/berkeley-db/%{name}-%{version}.tar.gz
%define sha1 db=5ae05c6c4a1766270fd5cfb28539e2b7a19c33b2
Group:		Databases
Vendor:		VMware, Inc.
Distribution:	Photon
%description
The Berkeley DB package contains programs and utilities used by many other applications for database related functions.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications 

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

%files docs
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*


%changelog
* 	Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 6.1.26-1
- 	Updated to version 6.1.26
* 	Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 5.3.28-2
-	Created devel sub-package. 
*	Sun Jan 04 2015 Touseef Liaqat <tliaqat@vmware.com> 6.1.19-1
-	Created separated docs package. First version
*	Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 6.1.19-1
-	Initial build. First version
