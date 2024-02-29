%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name rdiscount
%global ruby_ver 3.3.0

Name: rubygem-rdiscount
Version:        2.2.7.3
Release:        1%{?dist}
Summary:        Fast Implementation of Gruber's Markdown in C
Group:          Development/Languages
License:        BSD-3-CLAUSE
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  rdiscount=525791f2be10e118f556676a1645d2805ba6ad920e4f4c8761362c5aa09cf1f773f0216f7b6c2e1f78acbc1de1ac85c6088cc85729af70a28f537fdff3434786
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
%autosetup -p1 -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
gem install --bindir %{_bindir}/ %{gem_name}-%{version}.gem

%install
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}%{gemdir}/bin
mkdir -p %{buildroot}%{gemdir}/cache
mkdir -p %{buildroot}%{gemdir}/doc
mkdir -p %{buildroot}%{gemdir}/plugins
mkdir -p %{buildroot}%{gemdir}/specifications
mkdir -p %{buildroot}%{gemdir}/gems
mkdir -p %{buildroot}%{gemdir}/extensions/%{_arch}-linux/%{ruby_ver}
cp -pa %{_bindir}/rdiscount %{buildroot}%{gemdir}/bin/
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
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.2.7.3-1
-   Update to version 2.2.7.3
*   Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 2.2.7-1
-   Automatic Version Bump
*   Thu Sep 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.2.0.2-1
-   Initial build
