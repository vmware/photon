Summary:	Dos Filesystem tools
Name:		dosfstools
Version:	3.0.26
Release:	2%{?dist}
License:	GPLv3+
URL:		http://daniel-baumann.ch/software/dosfstools/
Group:		Filesystem Tools
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	http://daniel-baumann.ch/files/software/dosfstools/%{name}-%{version}.tar.gz
%define sha1 dosfstools=18a94a229867d9cb25d6c47c5c45563caa073cf0
%description
dosfstools contains utilities for making and checking MS-DOS FAT filesystems.
%prep
%setup -q
%build
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} PREFIX="/usr" install
%clean
rm -rf %{buildroot}/*
%files 
%defattr(-,root,root)
%{_sbindir}/*
%{_libdir}/*
%{_mandir}/man8/*
%{_docdir}/dosfstools/*
%exclude %{_mandir}/de/*
%exclude %{_libdir}/debug/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.0.26-2
-	GA - Bump release of all rpms
*	Wed Jul 1 2014 Sharath George <sharathg@vmware.com> 3.0.26-1
-	Initial build.	First version
