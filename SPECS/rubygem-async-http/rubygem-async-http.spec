%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async-http

Name:           rubygem-async-http
Version:        0.63.0
Release:        2%{?dist}
Summary:        A HTTP client and server library.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=6d98c0137860d010ef5da218ad06c39a529cbe9ce93e5740dc9608263eb1b0e062a59e7298da1f171d15dc00c06e6e50f876bcf39634c1f1f7d14971e8c6e796

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel
BuildRequires: rubygem-async
BuildRequires: rubygem-async-io
BuildRequires: rubygem-protocol-http
BuildRequires: rubygem-protocol-http1
BuildRequires: rubygem-protocol-http2
BuildRequires: rubygem-fiber-local
BuildRequires: rubygem-traces
BuildRequires: rubygem-async-pool

Requires: rubygem-async
Requires: rubygem-async-io >= 1.25.0, rubygem-async-io < 2.0.4
Requires: rubygem-protocol-http >= 0.24.0
Requires: rubygem-protocol-http1 >= 0.15.1
Requires: rubygem-protocol-http2 >= 0.15.0
Requires: rubygem-fiber-local
Requires: rubygem-traces
Requires: rubygem-async-pool
Requires: ruby

BuildArch: noarch

%description
An asynchronous client and server implementation of HTTP/1.0, HTTP/1.1 and HTTP/2
including TLS. Support for streaming requests and responses. Built on top of async
and async-io. falcon provides a rack-compatible server.

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.63.0-2
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.63.0-1
- Update to version 0.63.0
* Wed Oct 18 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.59.2-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 0.59.2-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.52.5-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.52.4-1
- Automatic Version Bump
* Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.48.2-1
- Initial build
