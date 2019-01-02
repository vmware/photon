# Generated from backports-2.5.1.gem by gem2rpm -*- rpm-spec -*-
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name backports

Name: rubygem-backports
Version:        3.7.0
Release:        2%{?dist}
Summary:        Backports of Ruby features for older Ruby
Group:          Development/Languages
License:        MIT
URL:            http://github.com/marcandre/backports
Source0:        https://rubygems.org/gems/backports-%{version}.gem
%define sha1    backports=66c9d715726d3fa2d6dbb818f4d09c652ae7cbc9
BuildRequires:  ruby

%description
Essential backports that enable many of the nice features of Ruby 1.8.7 up to
2.1.0 for earlier versions.

%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Tue Jan 29 2019 Srinidhi Rao <srinidhir@vmware.com> 3.7.0-2
-   Increment the release version as part of ruby upgrade.
*   Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 3.7.0-1
-   Updated to version 3.7.0.
*   Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 3.6.8-3
-   Bump up release number to reflect ruby upgrade
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.6.8-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 3.6.8-1
-   Upgrade version.
*   Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 3.6.7-1
-   Upgrade version.
*   Wed Nov 11 2015 Xiaolin Li <amakhalov@vmware.com> 3.6.4-1
-   Initial build
