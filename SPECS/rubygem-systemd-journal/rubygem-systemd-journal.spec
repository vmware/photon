%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name systemd-journal

Name: rubygem-systemd-journal
Version:        1.4.2
Release:        1%{?dist}
Summary:        Provides the ability to navigate and read entries from the systemd journal in ruby
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/systemd-journal-%{version}.gem
%define sha1    systemd-journal=68531140d09415377e0f64f450a52b94935e0618
BuildRequires:  ruby > 2.1.0

Requires: rubygem-ffi >= 1.9.0

Provides: rubygem-systemd-journal = %{version}

%description
Provides the ability to navigate and read entries from the systemd journal in ruby,
as well as write events to the journal.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.4.2-1
-   Automatic Version Bump
*   Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.3.3-1
-   Initial build
