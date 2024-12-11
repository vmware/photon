%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http-form_data

Name: rubygem-http-form_data
Version:        2.3.0
Release:        2%{?dist}
Summary:        Utility-belt to build form data request bodies. Provides support for application/x-www-form-urlencoded and multipart/form-data types.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  http-form_data=c070126d18a66bd505005d7dae4ece6c751e52593806daf618bbb437b7f9296a5f18aac2e317b3526c9b34adc2f4d9fc7b7bab8cf2a8c8ca67fdc5940969ff21

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby >= 1.9

BuildArch: noarch

%description
Utility-belt to build form data request bodies. Provides support for application/x-www-form-urlencoded and multipart/form-data types.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.3.0-2
-   Release bump for SRP compliance
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.0-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.0.3-2
-   rebuilt with ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.0.3-1
-   Initial build
