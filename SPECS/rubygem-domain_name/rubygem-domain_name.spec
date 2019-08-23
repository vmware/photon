%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name domain_name

Name: rubygem-domain_name
Version:        0.5.20190701
Release:        1%{?dist}
Summary:        This is a Domain Name manipulation library for Ruby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        BSD-2-Clause and BSD-3-Clause and MPLv2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    domain_name=c88205284700ac54a5b520f1358d341d76ecf77b
BuildRequires:  ruby

Requires: rubygem-unf >= 0.0.5, rubygem-unf < 1.0.0
BuildArch: noarch

%description
This is a Domain Name manipulation library for Ruby. It can also be used for
cookie domain validation based on the Public Suffix List.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.5.20190701-1
-   Initial build
