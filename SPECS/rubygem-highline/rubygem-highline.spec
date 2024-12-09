%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name highline

Name: rubygem-highline
Version: 2.0.3
Release: 2%{?dist}
Summary: A high-level IO library that provides validation, type conversion, and more for command-line interfaces
Group: Applications/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
URL: https://rubygems.org/gems/%{gem_name}
Source0: https://rubygems.org/downloads/highline-%{version}.gem
%define sha512 highline=18426c690125807ccc43af98d395c866752d2aa3a1d59ae2f16b65e3c207eedd76c0756f8acebdf4ceea2d52daf04500030f38e63f7658c39c946c6cb9737bb0

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby

Requires: ruby
%description
A high-level IO library that provides validation, type conversion, and more for command-line interfaces

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%check
cd %{buildroot}%{gemdir}/gems/highline-%{version}
gem install bundler code_statistics
LANG=en_US.UTF-8  rake test

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.0.3-2
-   Release bump for SRP compliance
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.3-1
-   Automatic Version Bump
*   Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 2.0.0-1
-   Update to version 2.0.0
* Tue Sep 05 2017 Chang Lee <changlee@vmware.com> 1.7.8-4
- Added %check
* Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 1.7.8-3
- Bump up release number to reflect ruby upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.8-2
- GA - Bump release of all rpms
* Wed Nov 11 2015 Anish Swaminathan <anishs@vmware.com> 1.7.8-1
- Initial build
