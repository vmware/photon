Summary:        VMware Photon OS 5.0 STIG Readiness Guide Ansible Playbook
Name:           stig-hardening
#Version x.y.z corresponds v<x>r<y>-z tag in the repo. Eg 1.1.1 = v1r1-1
Version:        1.1.1
Release:        1%{?dist}
License:        Apache-2.0
URL:            https://github.com/vmware/dod-compliance-and-automation/tree/master/photon/5.0/ansible/vmware-photon-5.0-stig-ansible-hardening
Group:          Productivity/Security
Vendor:         VMware, Inc.
Distribution:   Photon

#Update this URL to github URL once the source code is available in github
Source0: https://packages.vmware.com/photon/photon_sources/1.0/%{name}-ph5-%{version}.tar.gz
%define sha512 %{name}-ph5-%{version}=89ef1c4975c662c41ec147da72742c959f7479bf98de8709d65682bd5281e436fd05ee99a779e8edee0f6e56a72358df7fc1e6c3735e7fc9025756279117a5f6

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
rm -f %{_builddir}/%{name}-ph5-%{version}/vars-cap.yml
cp -rp %{_builddir}/%{name}-ph5-%{version}/ %{buildroot}%{_datadir}/ansible/%{name}

%files
%defattr(-,root,root,-)
%{_datadir}/ansible/

%changelog
* Wed Jun 28 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.1.1-1
- Minor version update
* Mon Jun 5 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.1-1
- Initial version
