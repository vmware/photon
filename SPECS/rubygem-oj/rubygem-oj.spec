%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name oj
%global ruby_ver 3.1.0

Name: rubygem-oj
Version:        3.13.21
Release:        2%{?dist}
Summary:        The fastest JSON parser and object serializer.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  oj=9a1429cf6197a1ab7b679185dc48570d17bc387e1d62bf0758b36797976ba60c9fca0680af3b64c0b4e1c8e873fe4a892018f571644650fa32bd67a4d03a0c05
BuildRequires:  ruby >= 2.0
BuildRequires:  gmp-devel
Requires:       ruby

%description
The fastest JSON parser and object serializer.

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
mkdir -p %{buildroot}%{gemdir}/{cache,doc,plugins,specifications,gems,extensions/%{_arch}-linux/%{ruby_ver}}
cp -a %{gemdir}/build_info %{buildroot}%{gemdir}/
cp -a %{gemdir}/cache/%{gem_name}-%{version}.gem %{buildroot}%{gemdir}/cache/
cp -a %{gemdir}/doc/%{gem_name}-%{version} %{buildroot}%{gemdir}/doc/
cp -a %{gemdir}/plugins %{buildroot}%{gemdir}/
cp -a %{gemdir}/specifications/%{gem_name}-%{version}.gemspec %{buildroot}%{gemdir}/specifications/
cp -a %{gemdir}/gems/%{gem_name}-%{version} %{buildroot}%{gemdir}/gems/
cp -a %{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}/%{gem_name}-%{version} %{buildroot}%{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.13.21-2
-   Build from source
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 3.13.21-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 3.10.14-1
-   Automatic Version Bump
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 3.10.13-1
-   Automatic Version Bump
*   Wed Sep 4 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.3.10-2
-   Enabled build for non x86_64 build archs
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 3.3.10-1
-   Initial build
