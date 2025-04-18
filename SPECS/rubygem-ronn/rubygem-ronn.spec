%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name ronn

Name: rubygem-ronn
Version:        0.7.3
Release:        4%{?dist}
Summary:        manual authoring tool
Group:          Development/Languages
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=885418c88d5a1073f9457ea11e29d82d3bb40ad12506589ccfab83ad447445e41282c9688aba5646082ae5ecc6a047fa9439ffae14561152fc61a136474f611c

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-mustache
BuildRequires: rubygem-rdiscount
BuildRequires: rubygem-hpricot

Requires:       ruby
Requires:       rubygem-hpricot
Requires:       rubygem-mustache
Requires:       rubygem-rdiscount

%description
Ronn converts textfiles to standard roff-formatted UNIX manpages or HTML

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.7.3-4
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.7.3-3
- Bump Version to build with new ruby
* Fri Nov 25 2022 Shivani Agarwal <shivania2@vmware.com> 0.7.3-2
- Version bump to build with new ruby
* Thu Sep 17 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 0.7.3-1
- Initial build
