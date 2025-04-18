%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-http

Name: rubygem-protocol-http
Version:        0.26.1
Release:        2%{?dist}
Summary:        Provides abstractions to handle HTTP protocols.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=9b17cc9ed699cdef8965e3a92599ee328ddf9f0abcdb012682dc8af7de8b805a686e8035bd5f569b30d465e3ef28e5eec3eca74980a9a0591d8b4e319a0ab274

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel

Requires: ruby

BuildArch: noarch

%description
Provides abstractions for working with the HTTP protocol.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.26.1-2
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.26.1-1
- Update to version 0.26.1
* Sun Aug 21 2022 Gerrit Photon <photon-checkins@vmware.com> 0.23.12-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.20.1-1
- Automatic Version Bump
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.12.1-2
- Rebuild the gem with ruby-2.7.1
* Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.12.1-1
- Initial build
