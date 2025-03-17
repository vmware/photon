%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-gcs

Summary:        Google Cloud Storage output plugin for Fluentd.
Name:           rubygem-fluent-plugin-gcs
Version:        0.4.4
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-fluentd
BuildRequires: rubygem-google-cloud-storage

Requires: ruby
Requires: rubygem-fluentd
Requires: rubygem-google-cloud-storage

%description
Google Cloud Storage output plugin for Fluentd.

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
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.4.4-1
- Initial version.
