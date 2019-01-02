%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name highline
Name: rubygem-highline
Version: 1.7.8
Release: 4%{?dist}
Summary: A high-level IO library that provides validation, type conversion, and more for command-line interfaces
Group: Applications/Programming
License: BSD
URL: https://rubygems.org/gems/%{gem_name}
Source0: https://rubygems.org/downloads/highline-%{version}.gem
%define sha1 highline=23e27608e2fdabd7ef60ebca1fc82aa686c2e880
BuildRequires: ruby
Requires: ruby
%description
A high-level IO library that provides validation, type conversion, and more for command-line interfaces
%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
%files
%defattr(-,root,root,-)
%{gemdir}
%changelog
* Tue Jan 29 2019 Srinidhi Rao <srinidhir@vmware.com> 1.7.8-4
- Increment the release version as part of ruby upgrade.
* Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 1.7.8-3
- Bump up release number to reflect ruby upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.8-2
- GA - Bump release of all rpms
* Wed Nov 11 2015 Anish Swaminathan <anishs@vmware.com> 1.7.8-1
- Initial build

