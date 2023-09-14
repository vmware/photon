Summary:        VMware Photon OS 5.0 STIG Readiness Guide Ansible Playbook
Name:           stig-hardening
#Version x.y.z corresponds v<x>r<y>-z tag in the repo. Eg 1.1.1 = v1r1-1
Version:        1.2
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/vmware/dod-compliance-and-automation/tree/master/photon/5.0/ansible/vmware-photon-5.0-stig-ansible-hardening
Group:          Productivity/Security
Vendor:         VMware, Inc.
Distribution:   Photon

#Remove these files from gitrepo while preparing tar ball
#.ansible-lint .gitignore .yamllint .gitattributes .gitlab-ci.yml vars-cap.yml
#Update this URL to github URL once the source code is available in github
Source0: https://packages.vmware.com/photon/photon_sources/1.0/%{name}-ph5-%{version}.tar.gz
%define sha512 %{name}-ph5-%{version}=683bdc6cbd951444dc6d08893e44c6d5de99a20e7eb603a1b96637ef71ddb635656582b8b07cb34c2e84af89a0ed0efc5cf8ae851a3f919e866eef77e6e068c6

Patch0: 0001-In-photon-5.0-.rpm.lock-file-path-has-changed.patch

BuildArch: noarch

Requires: ansible >= 2.14.2
Requires: ansible-community-general
Requires: ansible-posix
Requires: sshpass

%description
VMware Photon OS 5.0 STIG Readiness Guide Ansible Playbook

%prep
%autosetup -p1 -n %{name}-ph5-%{version}

%install
install -d %{buildroot}%{_datadir}/ansible/
cp -rp %{_builddir}/%{name}-ph5-%{version}/ %{buildroot}%{_datadir}/ansible/%{name}

%files
%defattr(-,root,root,-)
%{_datadir}/ansible/

%changelog
* Thu Sep 14 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.2-1
- update to 1.2 version
* Mon Jul 17 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.1.2-1
- Minor version update
* Wed Jun 28 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.1.1-1
- Minor version update
* Mon Jun 5 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.1-1
- Initial version
