%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-remote_syslog

Name:           rubygem-fluent-plugin-remote_syslog
Summary:        Fluentd output plugin for remote syslog
Version:        1.1.0
Release:        1%{?dist}
License:        MIT
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

BuildArch:      noarch

%define sha512  fluent-plugin-remote_syslog=19def4d336469ce254e50171e37e47cfbe616afe63ceb30606fcc852aae224eedaa7cbbc235a68094ee505229cb24ecb8a19137cf5708916de8ec311f283adf6

BuildRequires:  ruby >= 2.1

Requires: rubygem-fluentd >= 0
Requires: rubygem-remote_syslog_sender >= 1.1.1
Requires: ruby

%description
Fluentd plugin for remote syslog protocol

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Tue Jan 09 2024 Shivani Agrwal <shivania2@vmware.com> 1.1.0-1
-   Fixed requires and upgraded version
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.0.0-2
-   Rebuilt using ruby-2.7.1
*   Mon Jan 27 2020 Nikolay Stanchev <nstanchev@vmware.com> 1.0.0-1
-   Initial build
