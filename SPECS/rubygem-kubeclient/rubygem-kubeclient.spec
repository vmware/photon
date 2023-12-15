%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name kubeclient

Name:           rubygem-kubeclient
Version:        4.10.1
Release:        2%{?dist}
Summary:        A client for Kubernetes REST api.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        MIT
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512  kubeclient=71b5dcaeb238802ac096282d031c05c89dd7c950a2cc863fb1fa4aef596909c0834b2c53c5a759085e47e2f3929838fe8473ca6debee4e2b74e31095745a8190

BuildRequires:  ruby
BuildRequires:  findutils

Requires:       rubygem-activesupport
Requires:       rubygem-http >= 3.0, rubygem-http < 5.1.1
Requires:       rubygem-recursive-open-struct > 1.1
Requires:       rubygem-rest-client
Requires:       rubygem-http >= 3.0, rubygem-http < 5.0
Requires:       rubygem-http-accept >= 1.7.0, rubygem-http-accept < 2.0
Requires:       rubygem-jsonpath
Requires:       ruby

BuildArch:      noarch

%description
A client for Kubernetes REST api.

%prep
%autosetup -n %{gem_name}-%{version}

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}
[ -d %{buildroot}%{_libdir} ] && find %{buildroot}%{_libdir} -type f -perm /022 -exec chmod go-w {} \;

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Fri Dec 15 2023 Shivani Agarwal <shivania2@vmware.com> 4.10.1-2
-   Fix requires
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 4.10.1-1
-   Automatic Version Bump
*   Thu Oct 14 2021 Stanislav Hadjiiski <hadjiiskis@vmware.com> 4.9.1-2
-   Drop group write permissions for files in /usr/lib to comply with STIG
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 4.9.1-1
-   Automatic Version Bump
*   Wed Sep 02 2020 Sujay G <gsujay@vmware.com> 1.1.4-2
-   Rebuilt with ruby-2.7.1
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 1.1.4-1
-   Initial build
