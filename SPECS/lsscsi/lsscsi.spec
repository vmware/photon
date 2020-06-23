Summary:	List SCSI devices information.
Name:		lsscsi
Version:	0.31
Release:	1%{?dist}
License:	GPLv2
URL:		http://sg.danny.cz/scsi/lsscsi.html
Source0:	http://sg.danny.cz/scsi/%{name}-%{version}.tar.xz
%define sha1 lsscsi=b48ebea5656949c29498a55c3e899934661fa10c
Group:		Hardware/Others.
Vendor:		VMware, Inc.
Distribution:   Photon

%description
This lists the information about SCSI devices.

%prep
%setup -q -n lsscsi-%{version}

%build
%configure

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make %{?_smp_mflags} -k check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*

%changelog
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.31-1
- Automatic Version Bump
* Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.30-1
- Update to version 0.30
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.28-2
- GA - Bump release of all rpms
* Fri Apr 08 2016 Kumar Kaushik <kaushikk@vmware.com> 0.28-1
- Initial build. First version
