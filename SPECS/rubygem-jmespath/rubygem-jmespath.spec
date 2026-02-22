%global build_if %{photon_subrelease} >= 92
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name jmespath

Name: rubygem-jmespath
Version:        1.6.2
Release:        1%{?dist}
Summary:        Implements JMESPath for Ruby.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/jmespath-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
Implements JMESPath for Ruby.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Jan 19 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.6.2-1
- Update to version 1.6.2
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.6.1-4
- Spec bump with ruby upgrade
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.6.1-3
- Build gems properly
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.6.1-2
- Release bump for SRP compliance
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.6.1-1
- Automatic Version Bump
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.4.0-2
- rebuilt with ruby-2.7.1
* Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.4.0-1
- Initial build
