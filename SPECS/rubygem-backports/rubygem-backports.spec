# Generated from backports-2.5.1.gem by gem2rpm -*- rpm-spec -*-
%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name backports

Name: rubygem-backports
Version: 3.6.4
Release: 1%{?dist}
Summary: Backports of Ruby features for older Ruby
Group: Development/Languages
License: MIT
URL: http://github.com/marcandre/backports
Source0: https://rubygems.org/gems/backports-%{version}.gem
%define sha1 backports=06d3db9ac6e61b53d59dc197d5db3d7f8a4c312d
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
* Wed Nov 11 2015 Xiaolin Li <amakhalov@vmware.com> 3.6.4-1
- Initial build