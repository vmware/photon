%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name trollop
Name:           rubygem-trollop
Version:        2.9.10
Release:        2%{?dist}
Summary:        Commandline option parser for Ruby
Group:          Applications/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
URL: https://rubygems.org/gems/%{gem_name}
Source0: https://rubygems.org/downloads/trollop-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby

%if 0%{?with_check}
BuildRequires: git
%endif

Requires: ruby

%description
Commandline option parser for Ruby

%prep
%autosetup -c -T

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
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.9.10-2
- Release bump for SRP compliance
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.9.10-1
- Automatic Version Bump
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
