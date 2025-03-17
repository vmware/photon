Summary:        List SCSI devices information.
Name:           lsscsi
Version:        0.32
Release:        2%{?dist}
URL:            http://sg.danny.cz/scsi/lsscsi.html
Source0:        http://sg.danny.cz/scsi/%{name}-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}
Group:          Hardware/Others.
Vendor:         VMware, Inc.
Distribution:   Photon

%description
This lists the information about SCSI devices.

%prep
%autosetup

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
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 0.32-2
- Release bump for SRP compliance
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 0.32-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.31-1
- Automatic Version Bump
* Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 0.30-1
- Update to version 0.30
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.28-2
- GA - Bump release of all rpms
* Fri Apr 08 2016 Kumar Kaushik <kaushikk@vmware.com> 0.28-1
- Initial build. First version.
