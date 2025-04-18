%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name mime-types-data

Name: rubygem-mime-types-data
Version:        3.2022.0105
Release:        3%{?dist}
Summary:        Provides a registry for information about MIME media type definitions.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

BuildArch: noarch

%description
mime-types-data provides a registry for information about MIME media type definitions.
It can be used with the Ruby mime-types library or other software to determine defined
filename extensions for MIME types, or to use filename extensions to look up the likely
MIME type definitions.

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
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3.2022.0105-3
- Build gems properly
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.2022.0105-2
- Release bump for SRP compliance
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2022.0105-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 3.2020.0512-1
- Automatic Version Bump
* Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.2015.1120-1
- Initial build
