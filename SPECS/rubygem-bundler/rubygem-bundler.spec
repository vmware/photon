%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name bundler
%global ruby_ver 3.1.0

Name:           rubygem-bundler
Version:        2.3.24
Release:        2%{?dist}
Summary:        manages an application's dependencies
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/bundler-%{version}.gem
%define sha512  bundler=1d59bfa0bb8b748c8f4a7c30eb1603f05033bd59ca66496442224c563a95d8d8d2173e2f005a090a6b22e1a25664f20a3cf45b3d12ff7791712e327f194f242c
BuildRequires:  ruby > 2.1.0
BuildRequires:  findutils
Provides:       rubygem-bundler = %{version}

%description
Bundler manages an application's dependencies through its entire life
across many machines, systematically and repeatably.

%prep
gem unpack %{SOURCE0}
cd %{gem_name}-%{version}
/bin/chmod -Rf a+rX,u+w,g-w,o-w .
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
cd %{gem_name}-%{version}
gem build %{gem_name}.gemspec
gem install --bindir %{_bindir}/ %{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gemdir}/{bin,cache,doc,plugins,specifications,gems,extensions}
cp -a %{_bindir}/bundle %{_bindir}/bundler %{buildroot}%{gemdir}/bin/
cp -a %{gemdir}/cache/%{gem_name}-%{version}.gem %{buildroot}%{gemdir}/cache/
cp -a %{gemdir}/doc/%{gem_name}-%{version} %{buildroot}%{gemdir}/doc/
cp -a %{gemdir}/plugins %{buildroot}%{gemdir}/
cp -a %{gemdir}/specifications/%{gem_name}-%{version}.gemspec %{buildroot}%{gemdir}/specifications/
cp -a %{gemdir}/gems/%{gem_name}-%{version} %{buildroot}%{gemdir}/gems/
cp -a %{gemdir}/build_info %{buildroot}%{gemdir}/
[ -d %{buildroot}/usr/lib ] && find %{buildroot}/usr/lib -type f -perm /022 -exec chmod go-w {} \;

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.3.24-2
-   Build from source
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.3.24-1
-   Automatic Version Bump
*   Mon Nov 01 2021 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.2.21-2
-   Drop group write permissions for files in /usr/lib to comply with STIG
*   Fri Jul 02 2021 Piyush Gupta <gpiyush@vmware.com> 2.2.21-1
-   Upgrade to 2.2.21, Fixes CVE-2020-36327, CVE-2019-3881.
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.1.4-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.16.4-1
-   Update to version 1.16.4
*   Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.16.3-1
-   Initial build
