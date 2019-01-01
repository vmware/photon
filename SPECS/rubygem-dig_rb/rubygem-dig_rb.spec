%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name dig_rb

Name: rubygem-dig_rb
Version:        1.0.1
Release:        2%{?dist}
Summary:        Array/Hash/Struct#dig backfill for ruby
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/dig_rb-%{version}.gem
%define sha1    dig_rb=5ce0a66b0073c7c736cac61beafa4533d359df99
BuildRequires:  ruby
Provides: rubygem-dig_rb = %{version}

%description
Array/Hash/Struct#dig backfill for ruby

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Mon Feb 4 2019 Sujay G <gsujay@vmware.com> 1.0.1-2
-   Increment the release version as part of ruby upgrade
*   Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.1-1
-   Initial build
