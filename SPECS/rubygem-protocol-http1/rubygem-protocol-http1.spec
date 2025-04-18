%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-http1

Name:           rubygem-protocol-http1
Version:        0.18.0
Release:        2%{?dist}
Summary:        A low level implementation of the HTTP/1 protocol.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=8b557531f0fea005ab4ea0f02f407668ffb95f08f8807200b1e35bc6b0adf18dd6ea73833f78db60df77951f563a2451e71db8be02be1004a31efc88c25eb4d9

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-protocol-http
BuildRequires: rubygem-async-io
BuildRequires: rubygem-io-event

Requires: rubygem-protocol-http >= 0.5.0, rubygem-protocol-http < 1.0.0
Requires: rubygem-async-io
Requires: rubygem-io-event
Requires: ruby

BuildArch: noarch

%description
Provides a low-level implementation of the HTTP/1 protocol.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.18.0-2
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.18.0-1
- Update to version 0.18.0
* Sun Oct 22 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.14.6-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 0.14.6-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.13.1-1
- Automatic Version Bump
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.9.0-2
- Rebuilt with ruby-2.7.1
* Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.9.0-1
- Initial build
