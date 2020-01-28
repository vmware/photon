%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name syslog_protocol

Name:           rubygem-syslog_protocol
Summary:        Syslog Protocol
Version:        0.9.2
Release:        1%{?dist}
License:        MIT
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildArch:      noarch
%define sha1    syslog_protocol=024a76ac9bf2fec773e8c30601e161eca0406be4
BuildRequires:  ruby >= 2.1

%description
Syslog protocol parser and generator

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri May 29 2020 Nikolay Stanchev <nstanchev@vmware.com> 0.9.2-1
-   Initial build
