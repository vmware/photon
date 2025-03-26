%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluentd

Name: rubygem-fluentd
Version:        1.15.2
Release:        3%{?dist}
Summary:        An open source data collector designed to scale and simplify log management
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/fluentd-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: rubygem-thread_safe >= 0.1.0
Requires: rubygem-cool-io >= 1.4.5
Requires: rubygem-cool-io < 2.0.0
Requires: rubygem-dig_rb > 1.0.0
Requires: rubygem-http_parser.rb >= 0.5.1
Requires: rubygem-http_parser.rb < 0.8.1
Requires: rubygem-msgpack >= 0.5.11
Requires: rubygem-msgpack < 2
Requires: rubygem-sigdump >= 0.2.2
Requires: rubygem-strptime
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
Provides: rubygem(%{gem_name}) = %{version}-%{release}

%description
Fluentd is an open source data collector designed to scale and simplify log management.
It can collect, process and ship many kinds of data in near real-time.

%prep
%autosetup -c

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.15.2-3
-   Release bump for SRP compliance
*   Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 1.15.2-2
-   Add webrick to requires
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.15.2-1
-   Automatic Version Bump
*   Mon Jul 12 2021 Piyush Gupta <gpiyush@vmware.com> 1.11.3-2
-   Bump up to build with rubygem-bundler upgrade.
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
