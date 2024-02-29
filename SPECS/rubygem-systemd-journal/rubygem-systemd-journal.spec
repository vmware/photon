%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name systemd-journal

Name: rubygem-systemd-journal
Version:        1.4.2
Release:        2%{?dist}
Summary:        Provides the ability to navigate and read entries from the systemd journal in ruby
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/systemd-journal-%{version}.gem
%define sha512  systemd-journal=3eb2ef8b6ea4cf4f5f5e39d8aa9f1b5f6849a5037ab60b5b0a86a183be8d7b2354d61fe613194a6b695c44765771310830efa072fdc1834a9c20235ccb05f40c
BuildRequires:  ruby > 2.1.0

Requires: rubygem-ffi >= 1.9.0

Provides: rubygem-systemd-journal = %{version}

%description
Provides the ability to navigate and read entries from the systemd journal in ruby,
as well as write events to the journal.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.2-2
-   Bump Version to build with new ruby
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.2-1
-   Automatic Version Bump
*   Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.3.3-1
-   Initial build
