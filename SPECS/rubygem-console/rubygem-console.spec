%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name console

Summary:        Beautiful logging for Ruby.
Name:           rubygem-console
Version:        1.23.4
Release:        2%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=bd7e51e3fccd639961c54ce19b80ddc57483b2b444d660d03d87e37f7a9b6bbb0745d572d360411925746608e77f02fd734f5a476bdeff39990ecc3faaebbb75

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-fiber-local
BuildRequires: rubygem-fiber-annotation

Requires: ruby
Requires: rubygem-fiber-local
Requires: rubygem-fiber-annotation

BuildArch: noarch

%description
Provides beautiful console logging for Ruby applications. Implements fast, buffered log output.

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
*   Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.23.4-2
-   Build gems properly
*   Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.23.4-1
-   Update to version 1.23.4
* Thu Oct 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.16.2-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.16.2-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.9.0-1
- Automatic Version Bump
* Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.4.0-1
- Initial build
