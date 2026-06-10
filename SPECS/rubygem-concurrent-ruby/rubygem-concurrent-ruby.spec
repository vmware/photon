%global build_if %{photon_subrelease} >= 91
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name concurrent-ruby

Name: rubygem-concurrent-ruby
Version:        1.3.6
Release:        3%{?dist}
Summary:        Modern concurrency tools for Rails framework.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/concurrent-ruby/versions/%{version}
Source0:        https://rubygems.org/downloads/concurrent-ruby-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

Provides:      rubygem-thread_safe <= 0.3.6-5
Obsoletes:     rubygem-thread_safe <= 0.3.6-5

BuildRequires: ruby-devel

Requires: ruby

%description
Modern concurrency tools including agents, futures, promises, thread pools, actors,
supervisors, and more. Inspired by Erlang, Clojure, Go, JavaScript, actors, and
classic concurrency patterns.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri Jun 05 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.3.6-3
- Enable obsoletes
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 1.3.6-2
- Extended to build for subrelease 91 and above
* Mon Jan 19 2026 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.3.6-1
- Update to version 1.3.6
* Tue May 06 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.3.4-1
- Upgrade to 1.3.4
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.10-3
- Build gems properly
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.10-2
- Release bump for SRP compliance
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.1.10-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.7-1
- Automatic Version Bump
* Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.5-1
- Initial build
