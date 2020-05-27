%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async

Name: rubygem-async
Version:        1.20.1
Release:        1%{?dist}
Summary:        Async provides a modern asynchronous I/O framework for Ruby, based on nio4r.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    async=0875af3bc230d0b341068b3511381a1a1e45fcfc
BuildRequires:  ruby >= 2.2.7

Requires: rubygem-console >= 1.0.0, rubygem-console < 2.0.0
Requires: rubygem-nio4r >= 2.3.0, rubygem-nio4r < 3.0.0
Requires: rubygem-timers >= 4.1.0, rubygem-timers < 5.0.0

BuildArch: noarch

%description
Async provides a modern asynchronous I/O framework for Ruby, based on nio4r.
It implements the reactor pattern, providing both IO and timer based events.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.20.1-1
-   Initial build
