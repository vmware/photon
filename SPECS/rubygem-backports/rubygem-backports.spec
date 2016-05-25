# Generated from backports-2.5.1.gem by gem2rpm -*- rpm-spec -*-
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name backports

Name: rubygem-backports
Version: 3.6.8
Release: 2%{?dist}
Summary: Backports of Ruby features for older Ruby
Group: Development/Languages
License: MIT
URL: http://github.com/marcandre/backports
Source0: https://rubygems.org/gems/backports-%{version}.gem
%define sha1 backports=5c9dd0d5552d242ee6bb338a9097e85f0a0a45d5
BuildRequires: ruby

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
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.6.8-2
-	GA - Bump release of all rpms
* Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 3.6.8-1
- Upgrade version.
* Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 3.6.7-1
- Upgrade version.
* Wed Nov 11 2015 Xiaolin Li <amakhalov@vmware.com> 3.6.4-1
- Initial build
