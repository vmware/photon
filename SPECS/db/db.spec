Summary:	DB-6.1.26
Name:		db
Version:	6.1.26
Release:	3%{?dist}
License:	Sleepycat License
URL:		https://oss.oracle.com/berkeley-db.html
Source0:	http://download.oracle.com/berkeley-db/%{name}-%{version}.tar.gz
%define sha1 db=5ae05c6c4a1766270fd5cfb28539e2b7a19c33b2
Source1:        http://prdownloads.sourceforge.net/tcl/tcl8.6.5-src.tar.gz
%define sha1 tcl=c3a50ea58dac00a3c7e83cb4a4651c40d0f55160
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
tar xf %{SOURCE1} --no-same-owner
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

%check
pushd tcl8.6.5/unix
./configure --enable-threads --prefix=%{_prefix}
make
make install
popd

cd build_unix
make cutest
./cutest -s  TestCallbackSetterAndGetter -s TestDbTuner -s TestEnvMethod -s TestPartial -s TestPartial  \
-s TestQueue -s TestChannel -s  TestEncryption -s TestKeyExistErrorReturn -s TestPartition -s TestDbHotBackup \
-s TestEnvConfig -s TestPreOpenSetterAndGetter

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
*       Wed Oct 05 2016 ChangLee <changlee@vmware.com> 6.1.26-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.1.26-2
-	GA - Bump release of all rpms
* 	Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> 6.1.26-1
- 	Updated to version 6.1.26
* 	Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 5.3.28-2
-	Created devel sub-package. 
*	Sun Jan 04 2015 Touseef Liaqat <tliaqat@vmware.com> 6.1.19-1
-	Created separated docs package. First version
*	Tue Nov 25 2014 Divya Thaluru <dthaluru@vmware.com> 6.1.19-1
-	Initial build. First version
