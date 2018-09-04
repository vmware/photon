%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name tzinfo

Name: rubygem-tzinfo
Version:        1.2.5
Release:        1%{?dist}
Summary:        Timezone related support for Ruby.
Group:          Development/Languages
License:        MIT
URL:            https://rubygems.org/gems/tzinfo/versions/%{version}
Source0:        https://rubygems.org/downloads/tzinfo-%{version}.gem
%define sha1    tzinfo=c63e819a4ef646956bef31acec7d39ddccaff35c
BuildRequires:  ruby

%description
TZInfo provides daylight savings aware transformations between times in different time zones.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Tue Aug 14 2018 Srinidhi Rao <srinidhir@vmware.com> 1.2.5-1
-   Upgraded to 1.2.5
*   Fri Aug 25 2017 Kumar Kaushik <kaushikk@vmware.com> 1.2.3-1
-   Initial build
