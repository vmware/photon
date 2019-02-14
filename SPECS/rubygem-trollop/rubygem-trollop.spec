%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name trollop
Name:           rubygem-trollop
Version:        2.9.9
Release:        2%{?dist}
Summary:        Commandline option parser for Ruby
Group:          Applications/Programming
License:        BSD
Vendor:         VMware, Inc.
Distribution:   Photon
URL: https://rubygems.org/gems/%{gem_name}
Source0: https://rubygems.org/downloads/trollop-%{version}.gem
%define sha1 trollop=744730e58c4c56b5d652e210cb36974593eb1556
BuildRequires: ruby
%if %{with_check}
BuildRequires: git
%endif
Requires: ruby
%description
Commandline option parser for Ruby
%prep
%setup -q -c -T
%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%check
cd %{buildroot}%{gemdir}/gems/trollop-%{version}
gem install bundler chronic
rake test

%files
%defattr(-,root,root,-)
%{gemdir}
%changelog
* Tue Nov 27 2018 Sujay G <gsujay@vmware.com> 2.9.9-2
- Added %check section
* Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 2.9.9-1
- Update to version 2.9.9
* Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 2.1.2-3
- Bump up release number to reflect ruby upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.2-2
- GA - Bump release of all rpms
* Wed Nov 11 2015 Alexey Makhalov <amakhalov@vmware.com> 2.1.2-1
- Initial build

