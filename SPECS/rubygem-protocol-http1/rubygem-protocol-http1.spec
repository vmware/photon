%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name protocol-http1

Name: rubygem-protocol-http1
Version:        0.9.0
Release:        2%{?dist}
Summary:        A low level implementation of the HTTP/1 protocol.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    protocol-http1=ff0fc0e51e1fe4d42e535c234202fa567cd08c4d
BuildRequires:  ruby

Requires: rubygem-protocol-http >= 0.5.0, rubygem-protocol-http < 1.0.0

BuildArch: noarch

%description
Provides a low-level implementation of the HTTP/1 protocol.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 0.9.0-2
-   Rebuilt with ruby-2.7.1
*   Wed Aug 21 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 0.9.0-1
-   Initial build
