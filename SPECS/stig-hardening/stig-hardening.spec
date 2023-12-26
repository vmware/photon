Summary:        VMware Photon OS 4.0 STIG Readiness Guide Ansible Playbook
Name:           stig-hardening
#Version x.y.z corresponds v<x>r<y>-1 tag in the repo. Eg 1.1.1 = v1r1-1
Version:        1.5
Release:        2%{?dist}
License:        Apache-2.0
URL:            https://github.com/vmware/dod-compliance-and-automation/tree/master/photon/4.0/ansible/vmware-photon-4.0-stig-ansible-hardening
Group:          Productivity/Security
Vendor:         VMware, Inc.
Distribution:   Photon

# Remove these files while preparing the tar ball
# .gitattributes .gitignore .gitlab-ci.yml .yamllint .ansible-lint vars-cap.yml vars-vc8u2.yml
# Update this URL to github URL once the source code is available in github
Source0: https://packages.vmware.com/photon/photon_sources/1.0/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=61c14e97f27ca961edf48f94aadcd363eee40b2601a7016593ccb7914270cb23458c62960ea0d735bf6ad8367a367e094ce1d5722459d3d5667324a3d8791be9

BuildArch: noarch

Requires: ansible >= 2.12.7
Requires: ansible-community-general
Requires: ansible-posix
Requires: sshpass

%description
VMware Photon OS 4.0 STIG Readiness Guide Ansible Playbook

%prep
%autosetup -p1

%install
install -d %{buildroot}%{_datadir}/ansible/
cp -rp %{_builddir}/%{name}-%{version}/ %{buildroot}%{_datadir}/ansible/%{name}

%files
%defattr(-,root,root,-)
%{_datadir}/ansible/

%changelog
* Thu Jan 11 2024 Nitesh Kumar <kunitesh@vmware.com> 1.5-2
- Version bump up as a part of ansible v2.14.12 upgrade
* Mon Jan 08 2024 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.5-1
- Vesion update to 1.5
* Sat Sep 16 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.4.1-1
- Vesion update to 1.4.1
* Wed Aug 09 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.4-1
- Vesion update to 1.4
* Mon Jul 17 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.3.2-1
- Vesion update
* Wed Jun 28 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.3.1-1
- Vesion update
* Thu Feb 2 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.1-1
- Initial version
