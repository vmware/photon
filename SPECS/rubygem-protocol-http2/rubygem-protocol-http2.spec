%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-http2

Name: rubygem-protocol-http2
Version:        0.9.5
Release:        1%{?dist}
Summary:        A low level implementation of the HTTP/2 protocol.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    protocol-http2=6a43d96dc97ba340a3c424f46078c8152ad77102
BuildRequires:  ruby

Requires: rubygem-protocol-hpack >= 1.4.0, rubygem-protocol-hpack < 2.0.0
Requires: rubygem-protocol-http >= 0.2.0, rubygem-protocol-http < 1.0.0

BuildArch: noarch

%description
Provides a low-level implementation of the HTTP/2 protocol.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri May 29 2020 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.9.5-1
-   Initial build
