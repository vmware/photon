%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name remote_syslog_sender

Name:           rubygem-remote_syslog_sender
Summary:        Message sender that sends directly to a remote syslog endpoint (Support UDP, TCP, TCP+TLS)
Version:        1.2.1
Release:        2%{?dist}
License:        MIT
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
Patch0:         remote_syslog_sender-pr4.patch
BuildArch:      noarch
%define sha1    remote_syslog_sender=ee57147e8f597ab45126655078a1df93568f0792
BuildRequires:  ruby >= 2.1
Requires:       rubygem-syslog_protocol >= 0

%description
Message sender that sends directly to a remote syslog endpoint (Support UDP, TCP, TCP+TLS)

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
patch -d %{buildroot}/%{gemdir}/gems/%{gem_name}-%{version} -p1 < %{PATCH0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Mar 11 2020 Nikolay Stanchev <nstanchev@vmware.com> 1.2.1-2
*   Mon Jan 27 2020 Nikolay Stanchev <nstanchev@vmware.com> 1.2.1-1
-   Initial build
