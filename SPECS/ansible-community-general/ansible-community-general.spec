%global collection_namespace community
%global collection_name general

Summary:        Modules and plugins supported by Ansible community
Name:           ansible-community-general
Version:        5.6.0
Release:        1%{?dist}
License:        GPL-3.0-or-later AND BSD-2-Clause AND MIT AND PSF-2.0
URL:            https://github.com/ansible-collections/community.general
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/ansible-collections/community.general/archive/refs/tags/%{name}-%{version}.tar.gz
%define sha512  %{name}-%{version}=0551da11f47971214357ced770410613062c708a444d76dffc0a4702a9434a0bdd9542c37a8275d2975616f2bc9361b73db5c252e4407aba29720f51e317c48d

BuildArch:      noarch

BuildRequires:  ansible-devel

Requires:       ansible

%description
This repository contains the community.general Ansible Collection. The collection is a part of the
Ansible package and includes many modules and plugins supported by Ansible community which are not
part of more specialized community collections.

%prep
%autosetup -n community.general-%{version}
rm -vr .github .azure-pipelines
find -type f ! -executable -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +
find -type f -name '.gitignore' -print -delete

%build
%ansible_collection_build

%install
%ansible_collection_install
rm -vr %{buildroot}%{ansible_collection_files}/%{collection_name}/tests

%files
%defattr(-, root, root)
%license COPYING LICENSES
%doc README.md CHANGELOG.rst
%ansible_collection_files

%changelog
* Wed Sep 28 2022 Nitesh Kumar <kunitesh@vmware.com> 5.6.0-1
- Initial version
