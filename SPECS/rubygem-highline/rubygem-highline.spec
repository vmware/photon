%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name highline
Name:          rubygem-highline
Version:       3.0.1
Release:       1%{?dist}
Summary:       A high-level IO library that provides validation, type conversion, and more for command-line interfaces
Group:         Applications/Programming
License:       BSD
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           https://rubygems.org/gems/%{gem_name}
Source0:       https://rubygems.org/downloads/highline-%{version}.gem

%define sha512 highline=65b39f093cb26fac1cb256e8271ce3de98d010c6ceca55a5a782a768a024d40fee56c6b587ed0057cfe3b5451a6e6edf40c3ce50a02f9357b93a3f443d69dd80

BuildRequires: ruby

Requires:      ruby

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
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.0.1-1
- Update to version 3.0.1
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.3-1
- Automatic Version Bump
* Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 2.0.0-1
- Update to version 2.0.0
* Tue Sep 05 2017 Chang Lee <changlee@vmware.com> 1.7.8-4
- Added %check
* Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 1.7.8-3
- Bump up release number to reflect ruby upgrade
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.7.8-2
- GA - Bump release of all rpms
* Wed Nov 11 2015 Anish Swaminathan <anishs@vmware.com> 1.7.8-1
- Initial build
