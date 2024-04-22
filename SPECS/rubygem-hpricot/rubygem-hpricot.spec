%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name hpricot
%global ruby_ver 3.3.0

Name: rubygem-hpricot
Version:        0.8.6
Release:        3%{?dist}
Summary:        a swift, liberal HTML parser with a fantastic library
Group:          Development/Library
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  hpricot=f0ea9168ae79d099cdb751dd5a205e0896dfb229759e499fff833e94209d1497aa97becb285176dcbcc1fee19bc11913ca3ac0d7a467067e5d837c1eb6e310ad
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ruby

%description
Hpricot is a fast, flexible HTML parser written in C. It's designed to be
very accommodating and to have a very helpful library

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
*   Wed Feb 28 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.8.6-3
-   Update build command, to build with source code
*   Fri Nov 25 2022 Shivani Agarwal <shivania2@vmware.com> 0.8.6-2
-   Version bump to build with new ruby
*   Thu Sep 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.8.6-1
-   Initial build
