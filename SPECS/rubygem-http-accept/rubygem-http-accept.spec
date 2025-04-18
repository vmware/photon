%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name http-accept

Name:           rubygem-http-accept
Version:        1.7.0
Release:        3%{?dist}
Summary:        Parse Accept and Accept-Language HTTP headers.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=de263630227768a4cd5c8fa3b84eef54c6273ad207bc6958dd8b27dcee955ba3d6caf2972e9bd07f8aa03235d1ad9f260c1cdb66e83b24d69d0366fde28335b8

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

BuildArch: noarch

%description
Parse Accept and Accept-Language HTTP headers.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.7.0-3
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.7.0-2
- Bump Version to build with new ruby
* Fri Oct 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.7.0-1
- Initial version.
- Needed by rubygem-fluent-plugin-kubernetes_metadata_filter.
