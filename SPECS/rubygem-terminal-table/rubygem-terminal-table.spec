%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name terminal-table
Name: rubygem-terminal-table
Version: 1.5.2
Release: 2%{?dist}
Summary: Simple, feature rich ascii table generation library
Group: Applications/Programming
License: BSD
URL: https://rubygems.org/gems/%{gem_name}
Source0: https://rubygems.org/downloads/terminal-table-%{version}.gem
%define sha1 terminal=325ac67be9088df6386a951b72e45c0d95d52068
BuildRequires: ruby
Requires: ruby
%description
Simple, feature rich ascii table generation library
%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
%files
%defattr(-,root,root,-)
%{gemdir}
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.2-2
-	GA - Bump release of all rpms
* Wed Nov 11 2015 Alexey Makhalov <amakhalov@vmware.com> 1.5.2-1
- Initial build

