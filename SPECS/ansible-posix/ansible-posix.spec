%global collection_namespace ansible
%global collection_name posix

Summary:        Ansible Collection targeting POSIX and POSIX-ish platforms
Name:           ansible-posix
Version:        1.4.0
Release:        3%{?dist}
License:        GPLv3+ and Python
URL:            https://github.com/ansible-collections/ansible.posix
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/ansible-collections/ansible.posix/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=b78af6043c303a46bfab50745fdf1ae37a15c3060b97774890fb54dcc9ed05763085817cf8c12dc5e48ed0f46c68892a8c268883980c213b2d673ede63bde271

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
* Thu Jan 04 2024 Nitesh Kumar <kunitesh@vmware.com> 1.4.0-3
- Version bump up as a part of ansible v2.14.12 upgrade
* Thu Nov 24 2022 Nitesh Kumar <kunitesh@vmware.com> 1.4.0-2
- Version bump up to use ansible v2.12.7
* Wed Sep 28 2022 Nitesh Kumar <kunitesh@vmware.com> 1.4.0-1
- Initial version
