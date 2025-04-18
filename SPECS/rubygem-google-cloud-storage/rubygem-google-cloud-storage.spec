%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name google-cloud-storage

Summary:        google-cloud-storage is the official library for Google Cloud Storage.
Name:           rubygem-google-cloud-storage
Version:        1.54.0
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=f452fa61f23a0da1aaed1bbf718cff7dc296315290b60b0db63db55dc8bfc2c3e8a55163d5e2b9f76ea2faeed1b639d666e476bb6927c3aba676bb440aabaf2e

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-google-cloud-core
BuildRequires: rubygem-google-cloud-env
BuildRequires: rubygem-google-apis-storage_v1
BuildRequires: rubygem-google-apis-iamcredentials_v1
BuildRequires: rubygem-digest-crc
BuildRequires: rubygem-google-apis-core

Requires: ruby
Requires: rubygem-google-cloud-core
Requires: rubygem-google-cloud-env
Requires: rubygem-google-apis-storage_v1
Requires: rubygem-google-apis-iamcredentials_v1
Requires: rubygem-digest-crc
Requires: rubygem-google-apis-core

%description
google-cloud-storage is the official library for Google Cloud Storage.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.54.0-2
- Build gems properly
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.54.0-1
- Initial version. Needed by rubygem-fluent-plugin-gcs.
