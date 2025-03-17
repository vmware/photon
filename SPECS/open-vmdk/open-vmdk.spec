Summary:       Tools to create OVA files from raw disk images
Name:          open-vmdk
Version:       0.3.11
Release:       1%{?dist}
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://github.com/vmware/open-vmdk
Group:         Development/Tools

Source0:       https://github.com/vmware/open-vmdk/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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

%package -n ovfenv
Summary:       Tools to get or set OVF environment variables
Group:         Development/Tools
BuildArch:     noarch
Requires:      open-vm-tools
Requires:      python3
Requires:      python3-libxml2

%description -n ovfenv
Show the value of an OVF property, whether the properties
were presented to this VM in guestinfo or on a cdrom.
Optionally, allows a property value to be modified.

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
%{_bindir}/mkova.sh
%{_bindir}/ova-compose
%{_bindir}/vmdk-convert
%{_datadir}/%{name}/*

%files -n ovfenv
%defattr(-,root,root)
%{_bindir}/ovfenv

%changelog
* Tue Mar 11 2025 Oliver Kurth <oliver.kurth@broadcom.com> 0.3.11-1
- update to 0.3.11
- add ovfenv utility
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.3.10-2
- Release bump for SRP compliance
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
