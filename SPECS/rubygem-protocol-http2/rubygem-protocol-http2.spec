%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-http2

Name: rubygem-protocol-http2
Version:        0.14.1
Release:        1%{?dist}
Summary:        A low level implementation of the HTTP/2 protocol.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    protocol-http2=2b80d60044084a983929265c603cadca2dca647b
BuildRequires:  ruby

Requires: rubygem-protocol-hpack >= 1.4.0, rubygem-protocol-hpack < 2.0.0
Requires: rubygem-protocol-http >= 0.2.0, rubygem-protocol-http < 1.0.0

BuildArch: noarch

%description
Provides a low-level implementation of the HTTP/2 protocol.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.14.1-1
-   Automatic Version Bump
*   Wed Sep 2 2020 Sujay G <gsujay@vmware.com> 0.9.5-2
-   Rebuilt with ruby-2.7.1
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.9.5-1
-   Initial build
