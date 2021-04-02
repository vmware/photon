%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name net-http-persistent

Name:           rubygem-net-http-persistent
Summary:        Persistent connection management library
Version:        4.0.1
Release:        1%{?dist}
License:        MIT
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildArch:      noarch
%define sha1    net-http-persistent=1dfd87bfc8645e2f63c88b510ff5cc092c745006
BuildRequires:  ruby >= 2.3
Requires:       rubygem-connection_pool

%description
Manages persistent connections using Net::HTTP including a thread pool for connecting to multiple hosts.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri Apr 2 2021 Slav Danchev <sdanchev@vmware.com> 4.0.1-1
-   Initial build
