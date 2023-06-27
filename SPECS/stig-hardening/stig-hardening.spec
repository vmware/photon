Summary:        VMware Photon OS 4.0 STIG Readiness Guide Ansible Playbook
Name:           stig-hardening
#Version x.y.z corresponds v<x>r<y>-1 tag in the repo. Eg 1.1.1 = v1r1-1
Version:        1.3.1
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/vmware/dod-compliance-and-automation/tree/master/photon/4.0/ansible/vmware-photon-4.0-stig-ansible-hardening
Group:          Productivity/Security
Vendor:         VMware, Inc.
Distribution:   Photon

#Update this URL to github URL once the source code is available in github
Source0: https://packages.vmware.com/photon/photon_sources/1.0/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=2ad9cd42cc8cac83e79e261d9d9fc499c0a563f4906c3113cd078868cb35849b7a9a60cb7d9dc78fadbb668a23891bb8c317300bf76da9dbd79fe43fbe5be04a

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
rm -f %{_builddir}/%{name}-%{version}/vars-cap.yml
cp -rp %{_builddir}/%{name}-%{version}/ %{buildroot}%{_datadir}/ansible/%{name}

%files
%defattr(-,root,root,-)
%{_datadir}/ansible/

%changelog
* Wed Jun 28 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.3.1-1
- Vesion update
* Thu Feb 2 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.1-1
- Initial version
