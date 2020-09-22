%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http-form_data

Name: rubygem-http-form_data
Version:        2.3.0
Release:        1%{?dist}
Summary:        Utility-belt to build form data request bodies. Provides support for application/x-www-form-urlencoded and multipart/form-data types.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    http-form_data=1ed9996ba39ebebcb3102303cee7dc16de621f3f
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
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.3.0-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.0.3-2
-   rebuilt with ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.0.3-1
-   Initial build
