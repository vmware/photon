%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-http

Name: rubygem-protocol-http
Version:        0.24.0
Release:        1%{?dist}
Summary:        Provides abstractions to handle HTTP protocols.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  protocol-http=0822232df95723e73fa6bfb61a90509d2ca70b725692770c2bbe945f97d4900402ae36ea63b9651cde3a6860dfe970604fafb747e734a97c8b11218d9275815b
BuildRequires:  ruby >= 2.3.0

BuildArch: noarch

%description
Provides abstractions for working with the HTTP protocol.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri Nov 15 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.24.0-1
-   Bump version with the version upgrade of rubygem-async-http
*   Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.23.12-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.20.1-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.12.1-2
-   Rebuild the gem with ruby-2.7.1
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.12.1-1
-   Initial build
