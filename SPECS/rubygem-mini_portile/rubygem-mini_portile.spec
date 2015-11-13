%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name mini_portile

Name: rubygem-mini_portile
Version: 0.6.2
Release: 1%{?dist}
Summary: Simplistic port-like solution for developers
Group: Development/Languages
License: MIT
URL: https://rubygems.org/gems/mini_portile/
Source0: https://rubygems.org/downloads/mini_portile-%{version}.gem
%define sha1 mini_portile=696b940eb4ff8076a2080684046da1d2b10f41b8
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
* Wed Nov 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.6.2-1
- Initial build
