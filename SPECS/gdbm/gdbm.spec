Summary:	The GNU Database Manager
Name:		gdbm
Version:	1.13
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/gdbm
Group:		Applications/Databases
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnu.org/gnu/gdbm/%{name}-%{version}.tar.gz
%define sha1 gdbm=7f2a8301497bbcac91808b011ca533380914fd21

%description
This is a disk file format database which stores key/data-pairs in
single files. The actual data of any record being stored is indexed
by a unique key, which can be retrieved in less time than if it was
stored in a text file.

%prep
%setup -q

%build
./configure \
	--prefix=%{_prefix} \
	--enable-libgdbm-compat \
	--disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*
%{_mandir}/*/*

%changelog
*	Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 1.13-1
-	Upgrade gdbm to 1.13
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11-2
-	GA - Bump release of all rpms
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.11-1
-	Initial build.	First version
