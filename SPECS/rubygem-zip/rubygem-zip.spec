%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name zip

Name:           rubygem-zip
Version:        2.0.2
Release:        9%{?dist}
Summary:        Ruby library for reading and writing Zip files
Group:          Applications/Programming
Vendor:         VMware, Inc.
Distribution:   Photon
URL: https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/zip-%{version}.gem
%define sha512 %{gem_name}=5a4c16173d52dc59206d414e88d4f218373d8d145b2996d0c7099036a57f30acb69f18131a550be4fb9973f1b6cf4de53b82d1d9e5da4e375e81a482399867b5

Source1: license.txt
%include %{SOURCE1}

Patch0: 0001-add-file-exists-wrapper.patch

BuildRequires: ruby-devel
Requires: ruby

%description
Ruby library for reading and writing Zip files

%prep
%gem_unpack %{SOURCE0}
%autopatch -p1

%build
%gem_build

%install
%gem_install

%check
cd %{buildroot}%{gemdir}/gems/zip-%{version}
gem install jeweler
rake test

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.2-9
- Build gems properly
* Thu Jan 09 2025 Tapas Kundu <tapas.kundu@broadcom.com> 2.0.2-8
- Update License
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.0.2-7
- Release bump for SRP compliance
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 2.0.2-6
- Rebuilt using ruby-2.7.1
* Fri Jun 23 2017 Chang Lee <changlee@vmware.com> 2.0.2-5
- Updated %check
* Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 2.0.2-4
- Bump up release number to reflect ruby upgrade
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.0.2-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.2-2
- GA - Bump release of all rpms
* Wed Nov 11 2015 Anish Swaminathan <anishs@vmware.com> 2.0.2-1
- Initial build
