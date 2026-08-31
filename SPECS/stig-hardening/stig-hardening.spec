%global build_if %{photon_subrelease} >= 91

Summary:        VMware Photon OS 5.0 STIG Readiness Guide Ansible Playbook
Name:           stig-hardening
#Version x.y.z corresponds v<x>r<y>-z tag in the repo. Eg 1.1.1 = v1r1-1
Version:        2.1
Release:        9%{?dist}
URL:            https://github.com/vmware/dod-compliance-and-automation/tree/master/photon/5.0/ansible/vmware-photon-5.0-stig-ansible-hardening
Group:          Productivity/Security
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch: noarch

#Remove these files from gitrepo while preparing tar ball
#.ansible-lint .gitignore .yamllint .gitattributes .gitlab-ci.yml vars-cap.yml
#Update this URL to github URL once the source code is available in github
Source0: https://packages.broadcom.com/photon/photon_sources/1.0/%{name}-ph5-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0: fix-some-value-checks.patch
Patch1: system-auth-fix.patch
Patch2: fix-photon.yml-for-latest-audit-and-ansible.patch
Patch3: fix-stig-playbook-fips-pam.patch
Patch4: fix-selinux-relabel-first-boot.patch

Requires: ansible >= 2.20.1
Requires: ansible-community-general
Requires: ansible-posix
Requires: sshpass

%description
VMware Photon OS 5.0 STIG Readiness Guide Ansible Playbook

%prep
%autosetup -p1 -n %{name}-ph5-%{version}

%install
install -d %{buildroot}%{_datadir}/ansible/
cp -a %{_builddir}/%{name}-ph5-%{version}/ %{buildroot}%{_datadir}/ansible/%{name}

%files
%defattr(-,root,root,-)
%{_datadir}/ansible/

%changelog
* Sun Aug 30 2026 Daniel Casota <dcasota@gmail.com> 2.1-9
- Fix PHTN-50-000192 pam_faillock PAM stack corruption (| default guard)
- Add ima_hash=sha256 kernel parameter when fips=1 is active
- Generate fipsmodule.cnf when FIPS provider is present but config is missing
- Add first-boot SELinux relabel service for unlabeled filesystems (PR #9)
* Wed Jun 17 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.1-8
- Revisit system-auth fix, the previous fix was incomplete
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.1-7
- Extended to build for subrelease 91 and above
* Wed Apr 01 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.1-6
- Fix conditions for ansible-2.20 and audit-4.x
* Wed Mar 25 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.1-5
- Fix system auth rules
* Mon Feb 09 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.1-4
- Update URL to packages.broadcom.com
* Tue Nov 18 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.1-3
- Fix some validations
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
