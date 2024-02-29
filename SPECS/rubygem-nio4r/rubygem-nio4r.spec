%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name nio4r
%global ruby_ver 3.3.0

Name: rubygem-nio4r
Version:        2.7.0
Release:        1%{?dist}
Summary:        Cross-platform asynchronous I/O primitives for scalable network clients and servers.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  nio4r=aeb0bd3e727fa6999a314cd2b15a35035694f41294f7e9c406a72fd50a7a7a02311efec8c5795a116fd3793bf6b81e17d884e156b844722933e45d056f0cbeb9
BuildRequires:  gmp-devel
BuildRequires:  ruby >= 2.3.0
Requires:       ruby

%description
Cross-platform asynchronous I/O primitives for scalable network clients and servers.
Inspired by the Java NIO API, but simplified for ease-of-use.

%prep
gem unpack %{SOURCE0}
%autosetup -p1 -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
gem install %{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}%{gemdir}/cache
mkdir -p %{buildroot}%{gemdir}/doc
mkdir -p %{buildroot}%{gemdir}/plugins
mkdir -p %{buildroot}%{gemdir}/specifications
mkdir -p %{buildroot}%{gemdir}/gems
mkdir -p %{buildroot}%{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}
cp -pa %{gemdir}/build_info %{buildroot}%{gemdir}/
cp -pa %{gemdir}/cache/%{gem_name}-%{version}.gem %{buildroot}%{gemdir}/cache/
cp -pa %{gemdir}/doc/%{gem_name}-%{version} %{buildroot}%{gemdir}/doc/
cp -pa %{gemdir}/plugins %{buildroot}%{gemdir}/
cp -pa %{gemdir}/specifications/%{gem_name}-%{version}.gemspec %{buildroot}%{gemdir}/specifications
cp -pa %{gemdir}/gems/%{gem_name}-%{version} %{buildroot}%{gemdir}/gems
cp -pa %{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}/%{gem_name}-%{version} %{buildroot}%{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.7.0-1
-   Update to version 2.7.0
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.5.8-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.4-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.2-1
-   Automatic Version Bump
*   Wed Sep 4 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.4.0-2
-   Enabled build for non x86_64 build archs
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.4.0-1
-   Initial build
