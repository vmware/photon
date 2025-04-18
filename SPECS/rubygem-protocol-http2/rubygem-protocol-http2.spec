%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-http2

Name:           rubygem-protocol-http2
Version:        0.16.0
Release:        2%{?dist}
Summary:        A low level implementation of the HTTP/2 protocol.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=c0d34204b1c660129243c8fa10f9435b5857d89178f88b934bbf6ee0f698c2640612bbfc3b37ae10aa6be702fd795c226bb76d8614d2c7e0de21af0072823900

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-protocol-hpack
BuildRequires: rubygem-protocol-http
BuildRequires: rubygem-async-io
BuildRequires: rubygem-io-event

Requires: rubygem-protocol-hpack >= 1.4.0, rubygem-protocol-hpack < 2.0.0
Requires: rubygem-protocol-http >= 0.2.0, rubygem-protocol-http < 1.0.0
Requires: rubygem-async-io
Requires: rubygem-io-event
Requires: ruby

%description
Provides a low-level implementation of the HTTP/2 protocol.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.16.0-2
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.16.0-1
- Update to version 0.16.0
* Sun Oct 22 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.14.2-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 0.14.2-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.14.1-1
- Automatic Version Bump
* Wed Sep 2 2020 Sujay G <gsujay@vmware.com> 0.9.5-2
- Rebuilt with ruby-2.7.1
* Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.9.5-1
- Initial build
