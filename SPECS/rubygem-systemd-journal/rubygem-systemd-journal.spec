%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name systemd-journal

Name: rubygem-systemd-journal
Version:        1.4.2
Release:        2%{?dist}
Summary:        Provides the ability to navigate and read entries from the systemd journal in ruby
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/systemd-journal-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
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
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.4.2-2
-   Release bump for SRP compliance
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.2-1
-   Automatic Version Bump
*   Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.3.3-1
-   Initial build
