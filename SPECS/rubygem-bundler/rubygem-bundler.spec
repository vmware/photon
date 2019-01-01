%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name bundler

Name: rubygem-bundler
Version:        1.16.3
Release:        2%{?dist}
Summary:        manages an application's dependencies
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/bundler-%{version}.gem
%define sha1    bundler=ca6a670c29d2928a8dca24ee95a7978c8a532e36
BuildRequires:  ruby > 2.1.0
Provides: rubygem-bundler = %{version}

%description
Bundler manages an application's dependencies through its entire life
across many machines, systematically and repeatably.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 1.16.3-2
-   Increment the release version as part of ruby upgrade
*   Mon Aug 13 2018 Srinidhi Rao <srinidhir@vmware.com> 1.16.3-1
-   Initial build
