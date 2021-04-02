%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name connection_pool

Name:           rubygem-connection_pool
Summary:        Connection Pool
Version:        2.2.2
Release:        1%{?dist}
License:        MIT
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
BuildArch:      noarch
%define sha1    connection_pool=c95f97bc72de297b088327c8d5a257cba9a5256e
BuildRequires:  ruby >= 0

%description
Generic connection pool for Ruby

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri Apr 2 2021 Slav Danchev <sdanchev@vmware.com> 2.2.2-1
-   Initial build
