%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name hpricot

Name: rubygem-hpricot
Version:        0.8.6
Release:        2%{?dist}
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
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri Nov 25 2022 Shivani Agarwal <shivania2@vmware.com> 0.8.6-2
-   Version bump to build with new ruby
*   Thu Sep 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.8.6-1
-   Initial build
