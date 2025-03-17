%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name syslog_protocol

Name:           rubygem-syslog_protocol
Summary:        Syslog Protocol
Version:        0.9.2
Release:        3%{?dist}
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch

BuildRequires:  ruby >= 2.1

%description
Syslog protocol parser and generator

%prep
%autosetup -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Dec 11 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 0.9.2-3
-   Release bump for SRP compliance
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.9.2-2
-   Rebuilt using ruby-2.7.1
*   Mon Jan 27 2020 Nikolay Stanchev <nstanchev@vmware.com> 0.9.2-1
-   Initial build
