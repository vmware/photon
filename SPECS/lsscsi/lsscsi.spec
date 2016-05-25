Summary:	List SCSI devices information.
Name:		lsscsi
Version:	0.28
Release:	2%{?dist}
License:	GPLv2
URL:		http://sg.danny.cz/scsi/lsscsi.html
Source0:	http://sg.danny.cz/scsi/%{name}-%{version}.tar.xz
%define sha1 lsscsi=4a8db8bfb54d0eca6efa6cdc5dc6005381fce207
Group:		Hardware/Others.
Vendor:		VMware, Inc.
Distribution:   Photon

%description
This lists the information about SCSI devices.

%prep
%setup -q

%build
%configure

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	0.28-2
-	GA - Bump release of all rpms
*	Fri Apr 08 2016 Kumar Kaushik <kaushikk@vmware.com> 0.28-1
-	Initial build. First version
