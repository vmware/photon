%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name recursive-open-struct

Name: rubygem-recursive-open-struct
Version:        1.1.3
Release:        2%{?dist}
Summary:        A subclass of OpenStruct that allows nested hashes to be treated in a recursive fashion
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512    recursive-open-struct=f092c87a321a36eef2fff947383126f1da5865ab557c6cc359f91b1fe7e265d1cf7fa476d88ce5d2947bbfa63c8c956ac9a9487f249ef04977c94af04b8af8e3
BuildRequires:  ruby

BuildArch: noarch

%description
RecursiveOpenStruct is a subclass of OpenStruct. It differs from OpenStruct
in that it allows nested hashes to be treated in a recursive fashion.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.3-2
- Bump Version to build with new ruby
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.1.3-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.2-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.0.0-2
-   rebuilt with ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.0.0-1
-   Initial build
