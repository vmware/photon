%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name mini_portile2

Name: rubygem-mini_portile2
Version: 2.0.0
Release: 3%{?dist}
Summary: Simplistic port-like solution for developers
Group: Development/Languages
License: MIT
Source0: https://rubygems.org/downloads/mini_portile2-%{version}.gem
%define sha1 mini_portile2=a5845d50da195cb529d9ca114404920b7c401e07
BuildRequires: ruby
Requires: ruby
%description
Simplistic port-like solution for developers. It provides a standard and simplified way to compile against dependency libraries without messing up your system.

%prep
%setup -q -c -T
%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 2.0.0-3
- Bump up release number to reflect ruby upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.0-2
- GA - Bump release of all rpms
* Mon Mar 07 2016 Xiaolin Li <xiaolinl@vmware.com>
- Initial build
