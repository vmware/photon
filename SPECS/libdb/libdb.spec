Summary:	The Berkley DB database library for C
Name:		libdb
Version:	5.3.28
Release:	3%{?dist}
License:	BSD and LGPLv2 and Sleepycat
URL:		https://oss.oracle.com/berkeley-db.html
Source0:	http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
%define sha1 db=fa3f8a41ad5101f43d08bc0efb6241c9b6fc1ae9
Group:		System/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Obsoletes:      db
%description
The Berkeley DB package contains libraries used by many other applications for database related functions.

%package	utils
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	utils
db dump utility

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
Obsoletes:      db-devel
%description	devel
It contains the libraries and header files to create applications 

%package        docs
Summary:        DB docs
Group:          Databases
Obsoletes:      db-docs
%description docs
The package contains the DB doc files

%prep
%setup -q -n db-%{version}
%build
cd build_unix
../dist/configure \
	--host=%{_host} --build=%{_build} \
	--prefix=%{_prefix} \
	--enable-compat185 \
	--enable-dbm       \
	--disable-static
make %{?_smp_mflags}
%install
pushd build_unix
make DESTDIR=%{buildroot} docdir=%{_docdir}/%{name}-%{version} install
popd
find %{buildroot} -name '*.la' -delete
install -v -d -m755 %{buildroot}/%{_datadir}/licenses/
install -D -m755 LICENSE %{buildroot}/%{_datadir}/licenses/LICENSE
install -D -m755 README %{buildroot}/%{_datadir}/licenses/README

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%exclude %{_bindir}/*
%{_libdir}/*.so
%{_datadir}/licenses/*

%files utils
%defattr(-,root,root)
%{_bindir}/db_dump

%files docs
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}/*

%files devel
%defattr(-,root,root)
%exclude %{_includedir}/db_cxx.h
%{_includedir}/*

%changelog
*   Wed Jan 17 2018 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.3.28-3
-   add libdb-utils for db_dump
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 5.3.28-2
-   Aarch64 support
*	Thu Oct 27 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.3.28-1
-	Initial build. First version
