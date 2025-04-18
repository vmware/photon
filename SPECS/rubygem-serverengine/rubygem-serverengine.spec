%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name serverengine

Name:           rubygem-serverengine
Version:        2.3.2
Release:        2%{?dist}
Summary:        A framework to implement robust multiprocess servers like Unicorn
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/serverengine-%{version}.gem
%define sha512 %{gem_name}=9ca32740d4579fb8cbeb613780ed78a9a2e5a72fb427d24aa26a9a805f83de0d2840eb3de6e2e4205a771e1c58bcc4a171869807fdb49ddbb017ceeb8ca08c73

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel
BuildRequires:  rubygem-sigdump

Requires: ruby
Requires: rubygem-sigdump

%description
A framework to implement robust multiprocess servers like Unicorn.

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.3.2-2
-   Build gems properly
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.3.2-1
-   Update to version 2.3.2
* Mon Oct 23 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.3.0-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 2.3.0-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.2.1-1
- Automatic Version Bump
* Tue Jul 24 2018 Srinidhi Rao <srinidhir@vmware.com> 2.0.7-1
- Initial build
