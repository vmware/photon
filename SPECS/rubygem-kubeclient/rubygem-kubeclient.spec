%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name kubeclient

Name: rubygem-kubeclient
Version:        1.1.4
Release:        1%{?dist}
Summary:        A client for Kubernetes REST api.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    kubeclient=d0129e28ff280cf97316da6e3d9ce51e1e88bedd
BuildRequires:  ruby >= 2.0.0

Requires: rubygem-activesupport
Requires: rubygem-http = 0.9.8
Requires: rubygem-recursive-open-struct = 1.0.0
Requires: rubygem-rest-client
BuildArch: noarch

%description
A client for Kubernetes REST api.

%prep
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.1.4-1
-   Initial build
