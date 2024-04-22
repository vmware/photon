%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name rdiscount
%global ruby_ver 3.1.0

Name: rubygem-rdiscount
Version:        2.2.7
Release:        2%{?dist}
Summary:        Fast Implementation of Gruber's Markdown in C
Group:          Development/Languages
License:        BSD-3-CLAUSE
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  rdiscount=4f60dc0dbfb6b8f95f80d577c872c2a747d7d15e9fc1f1bd3640f1207a5d262068754dcb6d7b53348fd69de20b85534a390aace35d1eff31112bfbe0f77569d1
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ruby > 1.9.2
Requires:       ruby

%description
RDiscount converts documents in Markdown syntax to HTML.
It uses the excellent Discount processor by David Loren Parsons for this purpose,
and thereby inherits Discount’s numerous useful extensions to the Markdown language.

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
mkdir -p %{buildroot}%{gemdir}/{bin,cache,doc,plugins,specifications,gems,extensions/%{_arch}-linux/%{ruby_ver}}
cp -a %{_bindir}/bundle %{_bindir}/bundler %{buildroot}%{gemdir}/bin/
cp -a %{gemdir}/cache/%{gem_name}-%{version}.gem %{buildroot}%{gemdir}/cache/
cp -a %{gemdir}/doc/%{gem_name}-%{version} %{buildroot}%{gemdir}/doc/
cp -a %{gemdir}/plugins %{buildroot}%{gemdir}/
cp -a %{gemdir}/specifications/%{gem_name}-%{version}.gemspec %{buildroot}%{gemdir}/specifications/
cp -a %{gemdir}/gems/%{gem_name}-%{version} %{buildroot}%{gemdir}/gems/
cp -a %{gemdir}/build_info %{buildroot}%{gemdir}/
cp -a %{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}/%{gem_name}-%{version} %{buildroot}%{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.7-2
-   Build from source
*   Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 2.2.7-1
-   Automatic Version Bump
*   Thu Sep 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.2.0.2-1
-   Initial build
