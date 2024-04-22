%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name strptime
%global ruby_ver 2.7.0

Name: rubygem-strptime
Version:        0.2.5
Release:        2%{?dist}
Summary:        a fast strptime/strftime engine which uses VM
Group:          Development/Languages
License:        BSD 2
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/strptime-%{version}.gem
%define sha512  strptime=2f4493c6143f4984d7410c5b5270b8f93db211ae758ba3d5ca6f9e198733ad7e6d4d6996d9599f691b34d3329a242b99bd326767e52df0721b944e299ab03140
BuildRequires:  ruby
Provides: rubygem-strptime = %{version}

%description
a fast strptime/strftime engine which uses VM

%prep
gem unpack %{SOURCE0}
cd %{gem_name}-%{version}
/bin/chmod -Rf a+rX,u+w,g-w,o-w .
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
cd %{gem_name}-%{version}
gem build %{gem_name}.gemspec
gem install %{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gemdir}/{cache,doc,specifications,gems,extensions/%{_arch}-linux/%{ruby_ver}}
cp -a %{gemdir}/build_info %{buildroot}%{gemdir}/
cp -a %{gemdir}/cache/%{gem_name}-%{version}.gem %{buildroot}%{gemdir}/cache/
cp -a %{gemdir}/doc/%{gem_name}-%{version} %{buildroot}%{gemdir}/doc/
cp -a %{gemdir}/specifications/%{gem_name}-%{version}.gemspec %{buildroot}%{gemdir}/specifications/
cp -a %{gemdir}/gems/%{gem_name}-%{version} %{buildroot}%{gemdir}/gems/
cp -a %{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}/%{gem_name}-%{version} %{buildroot}%{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Apr 25 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.2.5-2
-   Build from source
*   Sat Sep 26 2020 Gerrit Photon <photon-checkins@vmware.com> 0.2.5-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.2.4-1
-   Automatic Version Bump
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 0.2.3-1
-   Initial build
