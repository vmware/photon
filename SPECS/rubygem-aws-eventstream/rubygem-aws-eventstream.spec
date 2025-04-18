%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name aws-eventstream

Name: rubygem-aws-eventstream
Version:        1.3.0
Release:        2%{?dist}
Summary:        Amazon Web Services event stream library.
Group:          Development/Languages
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/aws-eventstream-%{version}.gem
%define sha512 %{gem_name}=98200938fb087748010b494a75b3dc69c28903175631490cc529a5f740aef217e362eb77a98aa7ae3292e14a3cc559fe3f1f263293f536d47a515e7b77d8ddd8

Source1: license.txt
%include %{SOURCE1}

BuildRequires: ruby-devel

Requires: ruby

%description
Amazon Web Services event stream library.
Decodes and encodes binary stream under
`vnd.amazon.event-stream` content-type

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.3.0-2
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.3.0-1
- Update to version 1.3.0
* Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2.0-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.1.0-1
- Automatic Version Bump
* Mon Jul 30 2018 Srinidhi Rao <srinidhir@vmware.com> 1.0.1-1
- Initial build
