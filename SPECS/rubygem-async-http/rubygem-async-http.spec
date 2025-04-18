%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name async-http

Name: rubygem-async-http
Version:        0.60.2
Release:        3%{?dist}
Summary:        A HTTP client and server library.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

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

Requires: rubygem-async >= 1.19.0, rubygem-async < 2.2.2
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
* Mon Mar 03 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.60.2-3
- Build gems properly
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.60.2-2
- Release bump for SRP compliance
* Fri Nov 15 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.60.2-1
- Bump version with the version upgrade of rubygem-protocol-http1
* Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 0.59.2-2
- Fix requires
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 0.59.2-1
- Automatic Version Bump
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 0.52.5-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 0.52.4-1
- Automatic Version Bump
* Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.48.2-1
- Initial build
