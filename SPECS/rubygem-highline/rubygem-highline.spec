%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name highline
Name: rubygem-highline
Version: 2.0.0
Release: 1%{?dist}
Summary: A high-level IO library that provides validation, type conversion, and more for command-line interfaces
Group: Applications/Programming
License: BSD
URL: https://rubygems.org/gems/%{gem_name}
Source0: https://rubygems.org/downloads/highline-%{version}.gem
%define sha1 highline=56a3956394291617b22f77faa1aff0440ae60733
BuildRequires: ruby
Requires: ruby
%description
A high-level IO library that provides validation, type conversion, and more for command-line interfaces
%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%check
cd %{buildroot}%{gemdir}/gems/highline-%{version}
gem install bundler code_statistics
LANG=en_US.UTF-8  rake test

%files
%defattr(-,root,root,-)
%{gemdir}
%changelog
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 2.0.0-1
-   Update to version 2.0.0
* Tue Sep 05 2017 Chang Lee <changlee@vmware.com> 1.7.8-4
- Added %check
* Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 1.7.8-3
- Bump up release number to reflect ruby upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.8-2
- GA - Bump release of all rpms
* Wed Nov 11 2015 Anish Swaminathan <anishs@vmware.com> 1.7.8-1
- Initial build

