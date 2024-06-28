%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name oj

Name: rubygem-oj
Version:        3.13.21
Release:        1%{?dist}
Summary:        The fastest JSON parser and object serializer.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  oj=9a1429cf6197a1ab7b679185dc48570d17bc387e1d62bf0758b36797976ba60c9fca0680af3b64c0b4e1c8e873fe4a892018f571644650fa32bd67a4d03a0c05
BuildRequires:  ruby >= 2.0
BuildRequires:  gmp-devel
Requires:       ruby

%description
The fastest JSON parser and object serializer.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 3.13.21-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 3.10.14-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 3.10.13-1
-   Automatic Version Bump
*   Wed Sep 4 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.3.10-2
-   Enabled build for non x86_64 build archs
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.3.10-1
-   Initial build
