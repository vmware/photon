%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name connection_pool

Name:           rubygem-connection_pool
Version:        2.4.1
Release:        2%{?dist}
Summary:        An event loop.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=32a86ae3c11cf233038eb3d72ba24523b4ae2c21eab8cc9502806a768841b70d2fe98405e3fccb1c62df91ff06214d3a778353a8b76aa7e4e29659cf7aa72837

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

BuildArch: noarch

%description
Provides low level cross-platform primitives for constructing
event loops, with support for select, kqueue, epoll and io_uring.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.4.1-2
- Build gems properly
* Thu Apr 04 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 2.4.1-1
- Initial version. Needed by rubygem-activesupport.
