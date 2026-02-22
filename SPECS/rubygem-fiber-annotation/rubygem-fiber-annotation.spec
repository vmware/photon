%global build_if %{photon_subrelease} >= 92
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fiber-annotation

Summary:        A Ruby gem for annotating fibers with metadata
Name:           rubygem-fiber-annotation
Version:        0.2.0
Release:        2%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

BuildArch: noarch

%description
Fiber Annotation is a Ruby gem that provides an easy way to annotate fibers with metadata, making fiber management and debugging more efficient.

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
* Mon Jan 19 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.2.0-2
- bump version with ruby upgrade
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.2.0-1
- Initial version.
