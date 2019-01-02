%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name trollop
Name: rubygem-trollop
Version: 2.1.2
Release: 4%{?dist}
Summary: Commandline option parser for Ruby
Group: Applications/Programming
License: BSD
URL: https://rubygems.org/gems/%{gem_name}
Source0: https://rubygems.org/downloads/trollop-%{version}.gem
%define sha1 trollop=87a11bff3e9d08702487108cb18e01299112df44
BuildRequires: ruby
Requires: ruby
%description
Commandline option parser for Ruby
%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
%files
%defattr(-,root,root,-)
%{gemdir}
%changelog
* Tue Jan 29 2019 Srinidhi Rao <srinidhir@vmware.com> 2.1.2-4
- Increment the release version as part of ruby upgrade.
* Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 2.1.2-3
- Bump up release number to reflect ruby upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.2-2
- GA - Bump release of all rpms
* Wed Nov 11 2015 Alexey Makhalov <amakhalov@vmware.com> 2.1.2-1
- Initial build

