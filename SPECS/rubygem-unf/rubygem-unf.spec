%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name unf

Name: rubygem-unf
Version:        0.1.4
Release:        4%{?dist}
Summary:        This is a wrapper library to bring Unicode Normalization Form support to Ruby/JRuby.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=a4784afa8b852497f758d1b6cdcf095eb9e5397a36c97b1f22b53cf8077cfedbf83fdcda36f359acf59ba61f1ab8b706ddd31d097afbc98a40d2dbd0f934292b

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-unf_ext

Requires: rubygem-unf_ext
Requires: ruby

BuildArch: noarch

%description
This is a wrapper library to bring Unicode Normalization Form support to Ruby/JRuby.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.1.4-4
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.1.4-3
- Bump Version to build with new ruby
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.1.4-2
- rebuilt with ruby-2.7.1
* Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.1.4-1
- Initial build
