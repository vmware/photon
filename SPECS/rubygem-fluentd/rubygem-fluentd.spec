%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluentd

Name: rubygem-fluentd
Version:        1.15.3
Release:        1%{?dist}
Summary:        An open source data collector designed to scale and simplify log management
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache 2
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/fluentd-%{version}.gem
%define sha512  fluentd=74fa46527704b5c455831dd5a076bc395e6633eb599afcfcc1fd1a10581c59b020cd6c7405cfbc1c767c3bbbf39c9f126dccbcffd38974e80590d543009dd42a
BuildRequires:  ruby >= 2.1

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: rubygem-thread_safe >= 0.1.0
Requires: rubygem-cool-io >= 1.4.5
Requires: rubygem-cool-io < 2.0.0
Requires: rubygem-dig_rb > 1.0.0
Requires: rubygem-http_parser.rb >= 0.5.1
Requires: rubygem-http_parser.rb < 0.7.0
Requires: rubygem-msgpack >= 0.5.11
Requires: rubygem-msgpack < 2
Requires: rubygem-sigdump >= 0.2.2
Requires: rubygem-strptime > 0.2.2
Requires: rubygem-strptime < 1.0.0
Requires: rubygem-serverengine >= 2.0.4
Requires: rubygem-serverengine < 3.0.0
Requires: rubygem-tzinfo >= 1.0.0
Requires: rubygem-tzinfo-data > 1.0.0
Requires: rubygem-yajl-ruby >= 1.0
Requires: rubygem-bundler >= 1.14.0
Requires: rubygem-webrick >= 1.4.2, rubygem-webrick < 1.8.0
Requires: rubygem-concurrent-ruby
Requires: ruby

BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Fluentd is an open source data collector designed to scale and simplify log management.
It can collect, process and ship many kinds of data in near real-time.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Apr 16 2025 Mukul Sikka <mukul.sikka@broadcom.com> 1.15.3-1
-   upgrade to fix CVE-2022-39379
*   Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 1.15.2-1
-   Add webrick to requires and upgrade version
*   Thu Jul 08 2021 Piyush Gupta <gpiyush@vmware.com> 1.11.3-2
-   Version bump for rubygem-bundler upgrade.
*   Wed Sep 30 2020 Gerrit Photon <photon-checkins@vmware.com> 1.11.3-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.11.2-1
-   Automatic Version Bump
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.6.3-1
-   Update to version 1.6.3
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.2.5-1
-   Update to version 1.2.5
*   Thu Aug 16 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2.3-2
-   Added dependency on rubygem-bundler
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2.3-1
-   Initial build
