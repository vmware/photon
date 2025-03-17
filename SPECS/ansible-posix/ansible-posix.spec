%global collection_namespace ansible
%global collection_name posix

Summary:        Ansible Collection targeting POSIX and POSIX-ish platforms
Name:           ansible-posix
Version:        1.5.1
Release:        3%{?dist}
URL:            https://github.com/ansible-collections/ansible.posix
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/ansible-collections/ansible.posix/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch: noarch

BuildRequires: ansible-devel

Requires: ansible

%description
An Ansible Collection of modules and plugins that target POSIX UNIX/Linux and derivative Operating Systems.

%prep
%autosetup -n ansible.posix-%{version}
rm -vr tests/{integration,utils} \
       .github \
       changelogs/fragments/.keep \
       {test-,}requirements.txt \
       shippable.yml \
       .azure-pipelines

find -type f ! -executable -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +
find -type f -name '.gitignore' -print -delete

%build
export LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"
%{ansible_collection_build}

%install
export LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"
%{ansible_collection_install}

%files
%defattr(-, root, root)
%{ansible_collection_files}

%changelog
* Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 1.5.1-3
- Release bump for SRP compliance
* Tue Dec 26 2023 Nitesh Kumar <kunitesh@vmware.com> 1.5.1-2
- Version bump up as a part of ansible v2.14.12 upgrade
* Wed Feb 22 2023 Nitesh Kumar <kunitesh@vmware.com> 1.5.1-1
- Version upgrade to v1.5.1
* Fri Nov 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.4.0-2
- Bump version as a part of ansible upgrade
* Wed Sep 28 2022 Nitesh Kumar <kunitesh@vmware.com> 1.4.0-1
- Initial version
