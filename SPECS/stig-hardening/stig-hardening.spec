Summary:        VMware Photon OS 5.0 STIG Readiness Guide Ansible Playbook
Name:           stig-hardening
#Version x.y.z corresponds v<x>r<y>-z tag in the repo. Eg 1.1.1 = v1r1-1
Version:        1.2
Release:        4%{?dist}
License:        Apache-2.0
URL:            https://github.com/vmware/dod-compliance-and-automation/tree/master/photon/5.0/ansible/vmware-photon-5.0-stig-ansible-hardening
Group:          Productivity/Security
Vendor:         VMware, Inc.
Distribution:   Photon

#Remove these files from gitrepo while preparing tar ball
#.ansible-lint .gitignore .yamllint .gitattributes .gitlab-ci.yml vars-cap.yml
#Update this URL to github URL once the source code is available in github
Source0: https://packages.vmware.com/photon/photon_sources/1.0/%{name}-ph5-%{version}.tar.gz
%define sha512 %{name}-ph5-%{version}=762bf4b8b3922c07a65d41d49f6ebf581a2dcd22159fd1d4f0e38f5359834560e38a5507afd7dec576ad983c252d3ab2c53a6c91f5e8b70a3e321e0b74311628

Patch0: 0001-In-photon-5.0-.rpm.lock-file-path-has-changed.patch
Patch1: 0001-updates-to-support-running-on-chroot.patch
Patch2: 0002-adding-separate-task-to-copy-sysctl-tmpl.patch
Patch3: 0003-updating-template.patch

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
* Tue Dec 26 2023 Nitesh Kumar <kunitesh@vmware.com> 1.2-4
- Version bump as a part of ansible v2.16.2 upgrade
* Tue Oct 10 2023 Oliver Kurth <Mokurth@vmware.com> 1.2-3
- add chroot patches
* Fri Sep 22 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.2-2
- The stig-hardening source tarball is created by Photon OS team.
- If tar file is created in MAC and extracting same on Ubuntu, a duplicate
- file prefixed with “._” is created for each and every file present
- in tar file while extracting. Re uploaded correct source tar ball.
* Thu Sep 14 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.2-1
- update to 1.2 version
* Mon Jul 17 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.1.2-1
- Minor version update
* Wed Jun 28 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.1.1-1
- Minor version update
* Mon Jun 5 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.1-1
- Initial version
