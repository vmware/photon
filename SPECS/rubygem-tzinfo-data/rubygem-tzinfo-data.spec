%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name tzinfo-data

Name: rubygem-tzinfo-data
Version:        1.2026.5
Release:        1%{?dist}
Summary:        data from the IANA Time Zone database packaged as Ruby modules
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://rubygems.org/downloads/tzinfo-data-%{version}.gem
%define sha512 tzinfo-data=68ce9bbad24578ce44bcd5b3b44794065d69fb0ae3e26b34e80cd4c03c889288b5e31b4b30a02f50d97c7cb48996692c529929f347a5a381e478dd319656fe18

BuildRequires:  ruby

Requires: ruby
Requires: rubygem-tzinfo
Requires: rubygem-concurrent-ruby

Provides: rubygem-tzinfo-data = %{version}

%description
TZInfo::Data contains data from the IANA Time Zone database packaged as
Ruby modules for use with TZInfo.

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Oct 15 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.2026.5-1
-   Upgrade to v1.2026.5
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2020.1-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2018.5-1
-   Initial build
