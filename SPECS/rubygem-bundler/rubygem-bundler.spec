%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name bundler

Name:           rubygem-bundler
Version:        2.2.33
Release:        1%{?dist}
Summary:        manages an application's dependencies
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/bundler-%{version}.gem
%define sha1    bundler=32c50b62de0112d25d1c3491a8bcbb309ec83ea5
BuildRequires:  ruby > 2.1.0
BuildRequires:  findutils
Provides:       rubygem-bundler = %{version}

%description
Bundler manages an application's dependencies through its entire life
across many machines, systematically and repeatably.

%prep
%autosetup -n %{gem_name}-%{version}

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
[ -d %{buildroot}/usr/lib ] && find %{buildroot}/usr/lib -type f -perm /022 -exec chmod go-w {} \;

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 15 2021 Piyush Gupta <gpiyush@vmware.com> 2.2.33-1
-   Upgrade to 2.2.33.
*   Mon Nov 01 2021 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.2.21-2
-   Drop group write permissions for files in /usr/lib to comply with STIG
*   Thu Jul 08 2021 Piyush Gupta <gpiyush@vmware.com> 2.2.21-1
-   Upgrade to 2.2.21, Fixes CVE-2020-36327, CVE-2019-3881.
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.1.4-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.16.4-1
-   Update to version 1.16.4
*   Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.16.3-1
-   Initial build
