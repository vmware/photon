%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name concurrent-ruby

Name:           rubygem-concurrent-ruby
Version:        1.1.7
Release:        2%{?dist}
Summary:        Modern concurrency tools for Rails framework.
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/concurrent-ruby/versions/%{version}
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=037add9697ac36a2b7e24e39e6c11c1c7b593bd55bf0f3c3c56bdc320c05b05bcafefd463bb9211859e50851cc3858309d0cd5dacc4e521c1ca433dcf8956ba8

Patch0: CVE-2026-54906.patch

BuildRequires: ruby-devel

Requires: ruby

%description
Modern concurrency tools including agents, futures, promises, thread pools, actors,
supervisors, and more. Inspired by Erlang, Clojure, Go, JavaScript, actors, and
classic concurrency patterns.

%prep
%gem_unpack %{SOURCE0}
%patch -p1 0

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gem_base}

%changelog
* Mon Jun 29 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.7-2
- Fix CVE-2026-54906
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.7-1
- Automatic Version Bump
* Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.5-1
- Initial build
