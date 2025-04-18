%global debug_package %{nil}
%global gem_name kubeclient

Name:           rubygem-kubeclient
Version:        4.11.0
Release:        3%{?dist}
Summary:        A client for Kubernetes REST api.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=f32a9df1a0d56a2b128eb2377191ab61548d3873561eeaf46d6cb271d5b5ba29ca7a9df2dac6ff130c357e41ab2cfe6e307140c9255d2962f5ff5eb89c6ae144

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
gem install -V --local --force --install-dir %{buildroot}/%{gem_base} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gem_base}

%changelog
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 4.11.0-3
- Build gems properly
* Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.11.0-2
- Add gem macros
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.11.0-1
- Update to version 4.11.0
* Sat Oct 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.10.1-2
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
