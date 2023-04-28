Summary:        VMware Photon OS 3.0 STIG Readiness Guide Ansible Playbook
Name:           stig-hardening
#Version x.y corresponds v<x>r<y> tag in the repo. Eg 1.7 = v1r7
Version:        1.7
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/vmware/dod-compliance-and-automation/tree/master/photon/3.0/ansible/vmware-photon-3.0-stig-ansible-hardening
Group:          Productivity/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://packages.vmware.com/photon/photon_sources/1.0/%{name}-ph3-%{version}.tar.gz
%define sha512 %{name}-ph3-%{version}=69b0f453ad345ae9f6444893a43d507b7af0908727a4e9220839543822046bfc8eb5038e7a4d8cbac796bea552ec031c653ac100c7c05d47784ab26eea42a4f6

BuildArch: noarch

Requires: ansible >= 2.11.12
Requires: ansible-community-general
Requires: ansible-posix

%description
VMware Photon OS 3.0 STIG Readiness Guide Ansible Playbook

%prep
%autosetup -p1 -n %{name}-ph3-%{version}

%install
install -d %{buildroot}%{_datadir}/ansible/
cp -rp %{_builddir}/%{name}-ph3-%{version}/ %{buildroot}%{_datadir}/ansible/%{name}

%files
%defattr(-,root,root,-)
%{_datadir}/ansible/

%changelog
* Thu Feb 2 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.7-1
- Initial version
