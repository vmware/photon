%global debug_package %{nil}
%global gem_name fluent-plugin-kubernetes_metadata_filter

Name:           rubygem-fluent-plugin-kubernetes_metadata_filter
Version:        3.4.0
Release:        3%{?dist}
Summary:        Fluentd Filter plugin to add Kubernetes metadata.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache-2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha512 %{gem_name}=6383590639aab9a81aa87a191dcd5b7058e360dcf0ee7744e1a91b36e1c8b92f82a2f7de731883e208bb8e49d2dcc45285a714341e3fc226f1dfe4a8916c8bbf

BuildRequires:  ruby-devel
BuildRequires:  findutils

Requires:       rubygem-fluentd >= 0.14.0, rubygem-fluentd < 2.0.0
Requires:       rubygem-kubeclient < 5.0
Requires:       rubygem-http-accept >= 1.7.0, rubygem-http-accept < 2.0
Requires:       rubygem-http >= 3.0, rubygem-http < 5.0
Requires:       rubygem-lru_redux
Requires:       rubygem-jsonpath
Requires:       ruby

BuildArch:      noarch

%description
The Kubernetes metadata plugin filter enriches container log records with pod and namespace metadata.
This plugin derives basic metadata about the container that emitted a given log record using the source
of the log record. Records from journald provide metadata about the container environment as named fields.
Records from JSON files encode metadata about the container in the file name. The initial metadata derived
from the source is used to lookup additional metadata about the container's associated pod and namespace
(e.g. UUIDs, labels, annotations) when the kubernetes_url is configured. If the plugin cannot authoritatively
determine the namespace of the container emitting a log record, it will use an 'orphan' namespace ID in the
metadata. This behaviors supports multi-tenant systems that rely on the authenticity of the namespace for
proper log isolation.

%prep
%autosetup -n %{gem_name}-%{version}

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gem_base} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gem_base}

%changelog
*   Tue Apr 30 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.4.0-3
-   Add gem macros
* Mon Apr 22 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.4.0-2
- Build from source
*   Fri Dec 15 2023 Shivani Agrwal <shivania2@vmware.com> 3.4.0-1
-   Upgrade to v3.4.0
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 3.1.2-1
-   Automatic Version Bump
*   Thu Oct 14 2021 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.5.2-3
-   Drop group write permissions for files in /usr/lib to comply with STIG
*   Tue Sep 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.2-2
-   Update rubygem-kubeclient version
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.2-1
-   Automatic Version Bump
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.2.0-1
-   Initial build
