%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http-form_data

Name: rubygem-http-form_data
Version:        1.0.3
Release:        1%{?dist}
Summary:        Utility-belt to build form data request bodies. Provides support for application/x-www-form-urlencoded and multipart/form-data types.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    http-form_data=cc98987ba7d41c88ee26f90aacabdd1c0d53b336
BuildRequires:  ruby >= 1.9

BuildArch: noarch

%description
Utility-belt to build form data request bodies. Provides support for application/x-www-form-urlencoded and multipart/form-data types.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.0.3-1
-   Initial build
