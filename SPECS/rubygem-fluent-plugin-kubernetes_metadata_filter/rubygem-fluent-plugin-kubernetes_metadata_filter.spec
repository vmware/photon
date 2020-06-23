%global debug_package %{nil}
%global gemdir %(IFS=: R=($(gem env gempath)); echo ${R[${#R[@]}-1]})
%global gem_name fluent-plugin-kubernetes_metadata_filter

Name: rubygem-fluent-plugin-kubernetes_metadata_filter
Version:        2.5.2
Release:        1%{?dist}
Summary:        Fluentd Filter plugin to add Kubernetes metadata.
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache-2.0
URL:            https://rubygems.org/gems/%{gem_name}/versions/%{version}
Source0:        https://rubygems.org/downloads/%{gem_name}-%{version}.gem
%define sha1    fluent-plugin-kubernetes_metadata_filter=6e8b3dff1b227a2c22ba2796ad1885ce1fa67a77
BuildRequires:  ruby >= 2.1

Requires: rubygem-fluentd >= 0.14.0, rubygem-fluentd < 2.0.0
Requires: rubygem-kubeclient >= 1.1.4, rubygem-kubeclient < 1.2.0
Requires: rubygem-lru_redux
BuildArch: noarch

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
%setup -q -c -T

%build

%install
gem install -V --local --force --install-dir %{buildroot}/%{gemdir} %{SOURCE0}

%files
%defattr(-,root,root,-)
%{gemdir}

%changelog
*   Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 2.5.2-1
-   Automatic Version Bump
*   Thu Aug 22 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 2.2.0-1
-   Initial build
