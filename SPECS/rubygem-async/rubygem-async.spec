%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async

Name: rubygem-async
Version:        1.26.2
Release:        2%{?dist}
Summary:        Async provides a modern asynchronous I/O framework for Ruby, based on nio4r.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  async=1134cee7228056b745731c34c348736ac05c492abb0174dc557707a7d38b7564e6ee53ca1bdc9efcf23a514369d090a507cf5d80fdfc5da80153d759f802d644

BuildRequires:  ruby

Requires: rubygem-console >= 1.0.0, rubygem-console < 2.0.0
Requires: rubygem-nio4r >= 2.3.0, rubygem-nio4r < 3.0.0
Requires: rubygem-timers >= 4.1.0, rubygem-timers < 5.0.0
Requires: rubygem-fiber-local
Requires: ruby

BuildArch: noarch

%description
Async provides a modern asynchronous I/O framework for Ruby, based on nio4r.
It implements the reactor pattern, providing both IO and timer based events.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 1.26.2-2
-   Initial version. Needed by rubygem-async-http.
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.26.2-1
-   Automatic Version Bump
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.20.1-1
-   Initial build
