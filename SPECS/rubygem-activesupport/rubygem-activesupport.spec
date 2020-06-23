%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name activesupport

Name: rubygem-activesupport
Version:        6.0.3.2
Release:        1%{?dist}
Summary:        Support libaries for Rails framework.
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/activesupport/versions/%{version}
Source0:        https://rubygems.org/downloads/activesupport-%{version}.gem
%define sha1    activesupport=b92c473960b1ef01ee562d318604e1c8d1e6b175
BuildRequires:  ruby

%description
A toolkit of support libraries and Ruby core extensions extracted from the
Rails framework. Rich support for multibyte strings, internationalization,
time zones, and testing.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 6.0.3.2-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 5.2.1-1
-   Update to version 5.2.1
*   Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 5.0.0.1-1
-   Initial build
