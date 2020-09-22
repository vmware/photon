%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-http

Name: rubygem-protocol-http
Version:        0.20.1
Release:        1%{?dist}
Summary:        Provides abstractions to handle HTTP protocols.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    protocol-http=e653648353a4046db1665d86e668747cf9d7866c
BuildRequires:  ruby >= 2.3.0

BuildArch: noarch

%description
Provides abstractions for working with the HTTP protocol.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.20.1-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.12.1-2
-   Rebuild the gem with ruby-2.7.1
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.12.1-1
-   Initial build
