%global build_if %{photon_subrelease} >= 92
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name google-cloud-storage

Summary:        google-cloud-storage is the official library for Google Cloud Storage.
Name:           rubygem-google-cloud-storage
Version:        1.58.0
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

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
* Mon Jan 19 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.58.0-1
- Update to version 1.58.0
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.54.0-2
- Spec bump with ruby upgrade
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.54.0-1
- Initial version. Needed by rubygem-fluent-plugin-gcs.
