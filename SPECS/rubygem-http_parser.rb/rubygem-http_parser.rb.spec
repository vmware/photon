%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http_parser.rb

Name: rubygem-http_parser.rb
Version:        0.8.0
Release:        1%{?dist}
Summary:        Provides ruby bindings to http parser
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/http_parser.rb-%{version}.gem
%define sha512    http_parser.rb=228e8a617154411c43a548f10d2d8d2cae2d97970f621b4ef2955de94ed1943611cff22659cd75d63a09a0a02396993ab646ee29303d99856b46a80253a618c8
BuildRequires:  ruby
Provides: rubygem-http_parser.rb = %{version}

%description
Provides ruby bindings to http parser.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 0.8.0-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.6.0-2
-   rebuilt with ruby-2.7.1
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 0.6.0-1
-   Initial build
