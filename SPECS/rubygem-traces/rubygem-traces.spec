%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name traces

Name:           rubygem-traces
Version:        0.11.1
Release:        3%{?dist}
Summary:        Application instrumentation and tracing.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=1be8f690d6074b4f9c4f0df8465e9f1ebf059d89a9ba36579fa5e011d496244350f947d65d980a3b3d9f97b7f8eab069a97d24e6d4d67c6abad8d34c72b65b3c

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

BuildArch: noarch

%description
%{summary}

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.11.1-3
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.11.1-2
- Bump Version to build with new ruby
* Wed Oct 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.11.1-1
- Initial version. Needed by rubygem-async-http.
