%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name syslog_protocol

Name:           rubygem-syslog_protocol
Summary:        Syslog Protocol
Version:        0.9.2
Release:        4%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=cf94f495e57767517abfd8552baa09b284e016b03631871f72eb4aa5636958fea524c4f53c7d19b1b4fd7e1ee0f0c17297ce8a86d2b0e8efc3737018b2701646

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  ruby-devel

Requires: ruby

BuildArch: noarch

%description
Syslog protocol parser and generator

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.9.2-4
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.9.2-3
- Bump Version to build with new ruby
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.9.2-2
- Rebuilt using ruby-2.7.1
* Mon Jan 27 2020 Nikolay Stanchev <nstanchev@vmware.com> 0.9.2-1
- Initial build
