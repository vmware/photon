%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluentd

Name: rubygem-fluentd
Version:        1.2.3
Release:        3%{?dist}
Summary:        An open source data collector designed to scale and simplify log management
Group:          Development/Languages
License:        Apache 2
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/fluentd-%{version}.gem
%define sha1    fluentd=715fc88e66d0e2686b18a5c3c4787924c9281f40
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
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Fluentd is an open source data collector designed to scale and simplify log management.
It can collect, process and ship many kinds of data in near real-time.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 1.2.3-3
-   Increment the release version as part of ruby upgrade
*   Thu Aug 16 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2.3-2
-   Added dependency on rubygem-bundler
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2.3-1
-   Initial build
