%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name builder

Summary: Builders for MarkUp
Name: rubygem-builder
Version: 3.2.2
Release: 2%{?dist}
Group: Development/Languages
License: MIT
URL: http://onestepback.org
Source0: http://rubygems.org/gems/builder-%{version}.gem
%define sha1 builder=0ee99b207f9994864c2a21ce24be26eddafee7f1
BuildRequires: ruby
Requires: ruby

%description
Builder provides a number of builder objects that make creating structured
data simple to do. Currently the following builder objects are supported:

%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  3.2.2-2
-	GA - Bump release of all rpms
* Wed Nov 11 2015 Xiaolin Li <amakhalov@vmware.com> 3.2.2-1
- Initial build
