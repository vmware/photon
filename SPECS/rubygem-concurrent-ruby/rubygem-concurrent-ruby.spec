%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name concurrent-ruby

Name: rubygem-concurrent-ruby
Version:        1.1.10
Release:        2%{?dist}
Summary:        Modern concurrency tools for Rails framework.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/concurrent-ruby/versions/%{version}
Source0:        https://rubygems.org/downloads/concurrent-ruby-%{version}.gem

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  ruby

%description
Modern concurrency tools including agents, futures, promises, thread pools, actors,
supervisors, and more. Inspired by Erlang, Clojure, Go, JavaScript, actors, and
classic concurrency patterns.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.10-2
-   Release bump for SRP compliance
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.1.10-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.7-1
-   Automatic Version Bump
*   Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.5-1
-   Initial build
