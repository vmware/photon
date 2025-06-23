%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name webrick

Name:           rubygem-webrick
Version:        1.7.0
Release:        2%{?dist}
Summary:        HTTP server toolkit
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache 2
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0: https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=5f242b50300046fe7c22ecd1640a73e5815e05a72bedfebe6bc39c24c92bd61abdd180860de0d194c0eebbc640b507b6892de181d3b577c5372ace0ca6faf2a3

Patch0:         CVE-2024-47220.patch

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
* Mon Jun 23 2025 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.7.0-2
- Fix CVE-2024-47220
* Tue Jan 09 2024 Shivani Agarwal <shivania2@vmware.com> 1.7.0-1
- Initial version. Needed by rubygem-fluentd.
