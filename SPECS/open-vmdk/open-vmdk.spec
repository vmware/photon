Summary:       Tools to create OVA files from raw disk images
Name:          open-vmdk
Version:       0.3.10
Release:       1%{?dist}
Vendor:        VMware, Inc.
Distribution:  Photon
License:       Apache License 2.0
URL:           https://github.com/vmware/open-vmdk
Group:         Development/Tools

Source0:       https://github.com/vmware/open-vmdk/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}=a1b79ccf6e9fbbc9f92d58a756843303872d67bf6b0f99cb7bd4377bc3604b8c27b781b0e90598b3fbba552b813d4150672cee3444791e4f322a681dc1aed5e7

BuildRequires: zlib-devel

Requires: coreutils
Requires: grep
Requires: python3-lxml
Requires: python3-PyYAML
Requires: sed
Requires: tar
Requires: util-linux
Requires: zlib

%description
Tools to create OVA files from raw disk images. This includes 'vmdk-convert'
to create VMDKs from raw disk images, and 'ova-compose' to create OVA files
that can be imported by VMware vSphere or Fusion and Workstation.

%prep
%autosetup

%build
%make_build

%install
%make_install
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install templates/*.ovf %{buildroot}%{_datadir}/%{name}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/*
%{_datadir}/%{name}/*

%changelog
* Mon Jul 01 2024 Oliver Kurth <oliver.kurth@broadcom.com> 0.3.10-1
- update to 0.3.10
* Mon Apr 29 2024 Oliver Kurth <oliver.kurth@broadcom.com> 0.3.9-1
- update to 0.3.9
* Thu Mar 07 2024 Oliver Kurth <okurth@vmware.com> 0.3.8-1
- update to 0.3.8
* Fri Feb 02 2024 Oliver Kurth <okurth@vmware.com> 0.3.7-1
- update to 0.3.7
* Tue Nov 14 2023 Oliver Kurth <okurth@vmware.com> 0.3.6-1
- update to 0.3.6
* Thu Oct 26 2023 Oliver Kurth <okurth@vmware.com> 0.3.5-1
- update to 0.3.5
* Wed Sep 27 2023 Oliver Kurth <okurth@vmware.com> 0.3.3-1
- update to 0.3.3
* Tue Sep 19 2023 Oliver Kurth <okurth@vmware.com> 0.3.2-1
- update to 0.3.2
* Wed Jul 26 2023 Oliver Kurth <okurth@vmware.com> 0.3.1-1
- update to 0.3.1
* Wed Jul 12 2023 Oliver Kurth <okurth@vmware.com> 0.3.0-1
- update to 0.3.0
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.2.0-2
- Bump version as a part of zlib upgrade
* Fri Mar 17 2023 Oliver Kurth <okurth@vmware.com> 0.2.0-1
- update to 0.2.0
* Wed Feb 15 2023 Oliver Kurth <okurth@vmware.com> 0.1.0-1
- initial release
