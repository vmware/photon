%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%define gem_name rbvmomi

Summary:        Ruby interface to the VMware vSphere API.
Name:           rubygem-rbvmomi
Version:        3.0.0
Release:        3%{?dist}
Group:          Development/Languages
License:        MIT
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/vmware/%{gem_name}

Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=255a7517939a3d369244b7c66b39baa6903e489f8fd0057b4414850c5c90cf0a8931d507d8b5a7f806afba3c565a8cc5bba3b3cc614587d644f4060a165878ef

BuildRequires:  ruby

Requires: ruby
Requires: rubygem-builder
Requires: rubygem-nokogiri
Requires: rubygem-optimist

%description
RbVmomi is a Ruby interface to the vSphere API. Like the Perl and Java SDKs, you can use it to manage ESX and VirtualCenter servers. The current release supports the vSphere 5.0 API. RbVmomi specific documentation is online and is meant to be used alongside the official documentation.

%prep
%autosetup -p1 -n %{gem_name}-%{version}

%build
%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%check
cd %{buildroot}%{gemdir}/gems/rbvmomi-%{version}
gem install yard jeweler rake
rake test

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.0.0-3
- Bump Version to build with new ruby
* Mon Oct 23 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.0.0-2
- Fix requires
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0.0-1
- Automatic Version Bump
* Tue Sep 11 2018 srinidhira0 <srinidhir@vmware.com> 1.13.0-1
- Update to version 1.13.0
* Fri Jun 23 2017 Chang Lee <changlee@vmware.com> 1.10.0-2
- Updated %check
* Wed Mar 22 2017 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-1
- Updated to version 1.10.0.
* Wed Jan 25 2017 Anish Swaminathan <anishs@vmware.com> 1.8.2-4
- Bump up release number to reflect ruby upgrade
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.8.2-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.2-2
- GA - Bump release of all rpms
* Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.8.2-1
- Upgrade to 1.8.2
* Wed Nov 11 2015 Xiaolin Li <xiaolinl@vmware.com> 1.8.1-1
- Initial build
