%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name metrics

Summary:        Collects and exposes metrics from Ruby applications
Name:           rubygem-metrics
Version:        0.12.2
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

BuildArch:      noarch

%description
The `metrics` gem provides a lightweight framework for collecting, recording,
and reporting performance and operational metrics from Ruby applications.

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
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.12.2-1
- Initial version.
