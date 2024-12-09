%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-http1

Name: rubygem-protocol-http1
Version:        0.15.1
Release:        2%{?dist}
Summary:        A low level implementation of the HTTP/1 protocol.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  protocol-http1=7ecebe21b9d1177f1d0c232ce2d1eab17be0498eaeeab27e9083bea46038378d72cf9f55d8f2bb603ec93545ba7fd36cb9b5ecd54371ef3a9a9f07adeab77c55

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby

Requires: rubygem-protocol-http >= 0.5.0, rubygem-protocol-http < 1.0.0
Requires: rubygem-async-io
Requires: rubygem-io-event
Requires: ruby

BuildArch: noarch

%description
Provides a low-level implementation of the HTTP/1 protocol.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.15.1-2
-   Release bump for SRP compliance
*   Fri Nov 15 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.15.1-1
-   Fix CVE-2023-38697
*   Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 0.14.6-2
-   Fix requires
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 0.14.6-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.13.1-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.9.0-2
-   Rebuilt with ruby-2.7.1
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.9.0-1
-   Initial build
