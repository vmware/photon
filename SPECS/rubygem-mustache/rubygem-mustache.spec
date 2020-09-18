%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name mustache

Name: rubygem-mustache
Version:        1.1.1
Release:        1%{?dist}
Summary:        A framework-agnostic way to render logic-free views
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    mustache=52fafb63b70286bd197c5fa843c082798c1b8a85
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  ruby >= 2.0

%description
Mustache is a replacement for your views. Instead of views consisting of
ERB or HAML with random helpers and arbitrary logic, your views are broken
into two parts: a Ruby class and an HTML template

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Sep 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.1.1-1
-   Initial build
