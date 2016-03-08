%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name mini_portile

Name: rubygem-mini_portile2
Version: 2.0.0
Release: 1%{?dist}
Summary: Simplistic port-like solution for developers
Group: Development/Languages
License: MIT
Source0: https://rubygems.org/downloads/mini_portile2-%{version}.rc2.gem
%define sha1 mini_portile2=0128efd885c2628749e583831c611f368eeefb8f
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
* Mon Mar 07 2016 Xiaolin Li <xiaolinl@vmware.com>
- Initial build
