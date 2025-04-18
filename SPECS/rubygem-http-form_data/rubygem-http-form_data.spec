%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http-form_data

Name: rubygem-http-form_data
Version:        2.3.0
Release:        3%{?dist}
Summary:        Utility-belt to build form data request bodies. Provides support for application/x-www-form-urlencoded and multipart/form-data types.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=c070126d18a66bd505005d7dae4ece6c751e52593806daf618bbb437b7f9296a5f18aac2e317b3526c9b34adc2f4d9fc7b7bab8cf2a8c8ca67fdc5940969ff21

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel

Requires: ruby

BuildArch: noarch

%description
Utility-belt to build form data request bodies. Provides support for application/x-www-form-urlencoded and multipart/form-data types.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.3.0-3
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.3.0-2
- Bump Version to build with new ruby
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.0-1
- Automatic Version Bump
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.0.3-2
- rebuilt with ruby-2.7.1
* Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.0.3-1
- Initial build
