%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name remote_syslog_sender

Name:           rubygem-remote_syslog_sender
Summary:        Message sender that sends directly to a remote syslog endpoint (Support UDP, TCP, TCP+TLS)
Version:        1.2.2
Release:        2%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  remote_syslog_sender=f79af93c5fea6814ef03ba3d343205b3e3380bd1e6247b2fbd7881506df1dd219c47de992130e5666a3ac8fff753645e1c737b76f5f66b2e1c160c3d204de6b8

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  ruby >= 2.1

Requires:       rubygem-syslog_protocol >= 0

%description
Message sender that sends directly to a remote syslog endpoint (Support UDP, TCP, TCP+TLS)

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 1.2.2-2
-   Release bump for SRP compliance
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.2.2-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.2.1-3
-   Rebuilt using ruby-2.7.1
*   Wed Mar 11 2020 Nikolay Stanchev <nstanchev@vmware.com> 1.2.1-2
-   Add patch to prevent error raising when verify mode is VERIFY_NONE
*   Mon Jan 27 2020 Nikolay Stanchev <nstanchev@vmware.com> 1.2.1-1
-   Initial build
