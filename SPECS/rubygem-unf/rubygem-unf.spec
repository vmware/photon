%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name unf

Name: rubygem-unf
Version:        0.1.4
Release:        1%{?dist}
Summary:        This is a wrapper library to bring Unicode Normalization Form support to Ruby/JRuby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        BSD-2-Clause
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    unf=847ecaefb95c6639920a70e21812fad48c40fe08
BuildRequires:  ruby

Requires: rubygem-unf_ext
BuildArch: noarch

%description
This is a wrapper library to bring Unicode Normalization Form support to Ruby/JRuby.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.1.4-1
-   Initial build
