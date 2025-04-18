%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name webrick

Name:           rubygem-webrick
Version:        1.7.0
Release:        4%{?dist}
Summary:        HTTP server toolkit
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

Patch0:         CVE-2024-47220.patch
Patch1:         CVE-2025-6442.patch
# Follow-up fix for CVE-2025-6442
Patch2:         0001-Only-strip-space-and-horizontal-tab-in-headers.patch

BuildRequires:  ruby-devel

Requires: ruby

BuildArch: noarch

%description
WEBrick is an HTTP server toolkit that can be configured as an HTTPS server,
a proxy server, and a virtual-host server.

%prep
%gem_unpack %{SOURCE0}
%autopatch -p1

%build
%gem_build

%install
%gem_install

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
* Mon Sep 22 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.7.0-4
- Build gems properly
* Tue Sep 09 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.7.0-3
- Fix CVE-2025-6442 and CVE-2024-47220
* Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.7.0-2
- Release bump for SRP compliance
* Fri Oct 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.7.0-1
- Initial version. Needed by rubygem-fluentd.
