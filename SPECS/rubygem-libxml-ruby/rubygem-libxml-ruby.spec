%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name libxml-ruby
Name: rubygem-libxml-ruby
Version: 2.8.0
Release: 2%{?dist}
Summary: Provides Ruby language bindings for the GNOME Libxml2 XML toolkit
Group: Applications/Programming
License: BSD
URL: https://rubygems.org/gems/%{gem_name}
Source0: https://rubygems.org/downloads/libxml-ruby-%{version}.gem
%define sha1 libxml-ruby=6eb8d10c1ec340939bc0e5610a145e4933c67635
BuildRequires: ruby libxml2-devel 
Requires: ruby
%description
Provides Ruby language bindings for the GNOME Libxml2 XML toolkit
%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
%files
%defattr(-,root,root,-)
%{gemdir}
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.8.0-2
-	GA - Bump release of all rpms
* Wed Nov 11 2015 Anish Swaminathan <anishs@vmware.com> 2.8.0-1
- Initial build

