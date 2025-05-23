%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-remote_syslog

Name:           rubygem-fluent-plugin-remote_syslog
Summary:        Fluentd output plugin for remote syslog
Version:        1.1.0
Release:        3%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}

Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=19def4d336469ce254e50171e37e47cfbe616afe63ceb30606fcc852aae224eedaa7cbbc235a68094ee505229cb24ecb8a19137cf5708916de8ec311f283adf6

Source1: license.txt
%include %{SOURCE1}

BuildArch: noarch

BuildRequires: ruby-devel
BuildRequires: rubygem-remote_syslog_sender
BuildRequires: rubygem-fluentd

Requires: ruby
Requires: rubygem-fluentd
Requires: rubygem-remote_syslog_sender >= 1.1.1

%description
Fluentd plugin for remote syslog protocol

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
* Thu Apr 17 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.1.0-3
- Build gems properly
* Mon Feb 26 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.1.0-2
- Bump Version to build with new ruby
* Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 1.1.0-1
- Automatic Version Bump
* Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.0.0-2
- Rebuilt using ruby-2.7.1
* Mon Jan 27 2020 Nikolay Stanchev <nstanchev@vmware.com> 1.0.0-1
- Initial build
