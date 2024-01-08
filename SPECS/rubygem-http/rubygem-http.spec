%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http

Name:           rubygem-http
Version:        4.4.1
Release:        2%{?dist}
Summary:        An easy-to-use client library for making requests from Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  http=6e43a8ae379d7c8a807a9a03c87bfb5ad1719f9838e26ac7a695220ee2bc50344accc2db268d30da175328fd5468b87ec8532d17ce42a5b74d6c2c4c281d1bc9

BuildRequires:  ruby

Requires:       rubygem-addressable >= 2.3.0, rubygem-addressable < 3.0.0
Requires:       rubygem-http-cookie >= 1.0.0, rubygem-http-cookie < 2.0.0
Requires:       rubygem-http-form_data >= 2.2.0
Requires:       rubygem-http_parser.rb >= 0.6.0, rubygem-http_parser.rb < 0.7.0
Requires:       rubygem-llhttp-ffi
Requires:       ruby

BuildArch:      noarch

%description
An easy-to-use client library for making requests from Ruby. It uses a simple
method chaining system for building requests, similar to Python's Requests.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Jan 08 2024 Shivani Agarwal <shivania2@vmware.com> 4.4.1-2
-   Fix requires
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 4.4.1-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.9.8-2
-   rebuilt with ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.9.8-1
-   Initial build
