Summary:        VMware Photon OS 4.0 STIG Readiness Guide Ansible Playbook
Name:           stig-hardening
#Version x.y corresponds v<x>r<y> tag in the repo. Eg 1.1 = v1r1
Version:        1.1
Release:        1%{?dist}
License:        Apache-2.0
#Update this URL to github URL once the source code is available in github
URL:            https://packages.vmware.com/photon/photon_sources/1.0/%{name}-%{version}.tar.gz
Group:          Productivity/Security
Vendor:         VMware, Inc.
Distribution:   Photon

#Update this URL to github URL once the source code is available in github
Source0: https://packages.vmware.com/photon/photon_sources/1.0/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=fb7f57eacc68c129369b65494df8355bee1f1c0fc0dee5b73f056f2d6e1555d70b5d2f1644ab640e9213ba61e425e7897a83788cc1be9ab1cbc4ee05c0952d47

BuildArch: noarch

Requires: ansible >= 2.12.7
Requires: ansible-community-general
Requires: ansible-posix

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
* Thu Feb 2 2023 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.1-1
- Initial version
