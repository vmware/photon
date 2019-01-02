%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name zip
Name: rubygem-zip
Version: 2.0.2
Release: 4%{?dist}
Summary: Ruby library for reading and writing Zip files
Group: Applications/Programming
License: BSD
URL: https://rubygems.org/gems/%{gem_name}
Source0: https://rubygems.org/downloads/zip-%{version}.gem
%define sha1 zip=6fabc32da123f7013b2db804273df428a50bc6a4
BuildRequires: ruby
Requires: ruby
%description
Ruby library for reading and writing Zip files
%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
%files
%defattr(-,root,root,-)
%{gemdir}
%changelog
* Tue Jan 29 2019 Srinidhi Rao <srinidhir@vmware.com> 2.0.2-4
- Increment the release version as part of ruby upgrade.
* Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 2.0.2-3
- Bump up release number to reflect ruby upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.2-2
- GA - Bump release of all rpms
* Wed Nov 11 2015 Anish Swaminathan <anishs@vmware.com> 2.0.2-1
- Initial build

