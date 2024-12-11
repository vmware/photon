%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http-accept

Name: rubygem-http-accept
Version:        2.2.0
Release:        3%{?dist}
Summary:        Parse Accept and Accept-Language HTTP headers.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  http-accept=f60a9818e79b90c67da8b5c2a5f357b40049aec1809c0809bbf17e1c3d93734cd1367fd4d7d5afba1ae49f6c9817281b6892d6ef9a027d91fc49c46ec943409b

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby

Requires: ruby

BuildArch: noarch

%description
Parse Accept and Accept-Language HTTP headers.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.0-3
-   Release bump for SRP compliance
*   Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 2.2.0-2
-   Fix requires
*   Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 2.2.0-1
-   Automatic Version Bump
*   Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.0-3
-   Downgrade to 1.7.0 for rubygem-rest-client 2.1.0
*   Fri Sep 25 2020 Gerrit Photon <photon-checkins@vmware.com> 2.1.1-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.7.0-2
-   rebuilt with ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.7.0-1
-   Initial build
