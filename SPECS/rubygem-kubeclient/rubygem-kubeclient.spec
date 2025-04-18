%global debug_package %{nil}
%global gem_name kubeclient

Name:           rubygem-kubeclient
Version:        4.10.1
Release:        6%{?dist}
Summary:        A client for Kubernetes REST api.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildArch: noarch

BuildRequires:  ruby-devel
BuildRequires:  rubygem-activesupport
BuildRequires:  rubygem-http < 5.0
BuildRequires:  rubygem-recursive-open-struct
BuildRequires:  rubygem-jsonpath
BuildRequires:  rubygem-rest-client
BuildRequires:  rubygem-http-accept < 2.0
BuildRequires:  findutils

Requires:       rubygem-activesupport
Requires:       rubygem-recursive-open-struct > 1.1
Requires:       rubygem-rest-client
Requires:       rubygem-http < 5.0
Requires:       rubygem-http-accept < 2.0
Requires:       rubygem-jsonpath
Requires:       rubygem-ffi-compiler
Requires:       ruby

%description
A client for Kubernetes REST api.

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
* Thu Feb 27 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.10.1-6
- Bump version with rubygem-activesupport bump
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.10.1-5
- Release bump for SRP compliance
* Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.10.1-4
- Add gem macros
* Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.10.1-3
- Build from source
* Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 4.10.1-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 4.10.1-1
- Automatic Version Bump
* Thu Oct 14 2021 Stanislav Hadjiiski <hadjiiskis@vmware.com> 4.9.1-2
- Drop group write permissions for files in /usr/lib to comply with STIG
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 4.9.1-1
- Automatic Version Bump
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.1.4-2
- Rebuilt with ruby-2.7.1
* Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.1.4-1
- Initial build
