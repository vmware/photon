Summary:        VMware Photon OS 5.0 STIG Readiness Guide Ansible Playbook
Name:           stig-hardening
#Version x.y.z corresponds v<x>r<y>-z tag in the repo. Eg 1.1.1 = v1r1-1
Version:        2.1
Release:        2%{?dist}
URL:            https://github.com/vmware/dod-compliance-and-automation/tree/master/photon/5.0/ansible/vmware-photon-5.0-stig-ansible-hardening
Group:          Productivity/Security
Vendor:         VMware, Inc.
Distribution:   Photon

#Remove these files from gitrepo while preparing tar ball
#.ansible-lint .gitignore .yamllint .gitattributes .gitlab-ci.yml vars-cap.yml
#Update this URL to github URL once the source code is available in github
Source0: https://packages.vmware.com/photon/photon_sources/1.0/%{name}-ph5-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 2.1-2
- Release bump for SRP compliance
* Fri Aug 16 2024 Shivani Agarwal <shivani.agarwal@vmware.com> 2.1-1
- Update to 2.1 version
* Mon Jan 08 2024 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.3-1
- Update to 1.3 version
* Tue Dec 26 2023 Nitesh Kumar <kunitesh@vmware.com> 1.2-4
- Version bump up as a part of ansible v2.14.12 upgrade
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
