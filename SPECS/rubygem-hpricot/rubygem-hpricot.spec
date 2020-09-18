%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name hpricot

Name: rubygem-hpricot
Version:        0.8.6
Release:        1%{?dist}
Summary:        a swift, liberal HTML parser with a fantastic library
Group:          Development/Library
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    hpricot=87ce2c17960a5e1d7ceaa16d0591ca6a28379ce0
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ruby

%description
Hpricot is a fast, flexible HTML parser written in C. It's designed to be
very accommodating and to have a very helpful library

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Sep 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.8.6-1
-   Initial build
