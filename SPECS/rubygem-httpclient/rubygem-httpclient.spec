%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name httpclient

Summary:        Gives something like the functionality of libwww-perl (LWP) in Ruby
Name:           rubygem-httpclient
Version:        2.8.3
Release:        1%{?dist}
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=d02c7b7c9e1a386b6e16ebbf4b00ce916233a08cca7286f03c39aee0935fc5a811cb20c0613b50dff9dd8bd5d92d1a5c7e8d45fb724aeaa36bf90b597bd9d428

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
Gives something like the functionality of libwww-perl (LWP) in Ruby

%prep
%gem_unpack %{SOURCE0}

%build
%gem_build

%install
%gem_install

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Fri Feb 07 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.8.3-1
- Initial version.
