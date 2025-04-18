%global debug_package %{nil}
%global gem_name strptime

Name: rubygem-strptime
Version:        0.2.5
Release:        5%{?dist}
Summary:        a fast strptime/strftime engine which uses VM
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/strptime-%{version}.gem
%define sha512 %{gem_name}=2f4493c6143f4984d7410c5b5270b8f93db211ae758ba3d5ca6f9e198733ad7e6d4d6996d9599f691b34d3329a242b99bd326767e52df0721b944e299ab03140

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel

Requires:       ruby

%description
A fast strptime/strftime engine which uses VM

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gem_base}

%changelog
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.2.5-5
- Build gems properly
* Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.2.5-4
- Add gem macros
* Wed Feb 28 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.2.5-3
- Update build command, to build with source code
* Fri Nov 25 2022 Shivani Agarwal <shivania2@vmware.com> 0.2.5-2
- Version bump to build with new ruby
* Sat Sep 26 2020 Gerrit Photon <photon-checkins@vmware.com> 0.2.5-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.2.4-1
- Automatic Version Bump
* Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 0.2.3-1
- Initial build
