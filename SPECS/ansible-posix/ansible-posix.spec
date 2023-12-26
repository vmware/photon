%global collection_namespace ansible
%global collection_name posix

Summary:        Ansible Collection targeting POSIX and POSIX-ish platforms
Name:           ansible-posix
Version:        1.5.2
Release:        1%{?dist}
License:        GPLv3+ and Python
URL:            https://github.com/ansible-collections/ansible.posix
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/ansible-collections/ansible.posix/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=ace79735e9c061a9919ee39c5f561fe91407df1843d0de37378b2f0d721ab2cc33558bff7589fd428e7b1b19431972d7d0e9b390b7d6289cee2dae06bec1af38

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
* Tue Dec 26 2023 Nitesh Kumar <kunitesh@vmware.com> 1.5.2-1
- Version upgrade to v1.5.2
* Wed Feb 22 2023 Nitesh Kumar <kunitesh@vmware.com> 1.5.1-1
- Version upgrade to v1.5.1
* Fri Nov 25 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.4.0-2
- Bump version as a part of ansible upgrade
* Wed Sep 28 2022 Nitesh Kumar <kunitesh@vmware.com> 1.4.0-1
- Initial version
