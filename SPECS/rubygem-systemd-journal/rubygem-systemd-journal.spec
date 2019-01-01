%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name systemd-journal

Name: rubygem-systemd-journal
Version:        1.3.3
Release:        2%{?dist}
Summary:        Provides the ability to navigate and read entries from the systemd journal in ruby
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/systemd-journal-%{version}.gem
%define sha1    systemd-journal=3861d36e84af55a30418fc0909df623274250c66
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
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 1.3.3-2
-   Increment the release version as part of ruby upgrade
*   Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.3.3-1
-   Initial build
