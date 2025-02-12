%define srcname     buildx
%define plugins_dir %{_libexecdir}/docker/cli-plugins

Name:       docker-buildx
Summary:    Docker CLI plugin for extended build capabilities with BuildKit
Version:    0.17.1
Release:    1%{?dist}
URL:        https://github.com/docker/buildx
Group:      Applications
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/docker/buildx/archive/refs/tags/%{srcname}-%{version}.tar.gz
%define sha512 %{srcname}=16840bdfc79d4931253d2193ea43d9c47bc65e7f3049cecc27260ae98bc994637634fe7fa7333c01cd540205cd5c8aa73e65bee09f315098c15030bb799d172d

Source1: license.txt
%include %{SOURCE1}

BuildRequires: go

Requires: docker

%description
Docker CLI plugin for extended build capabilities with BuildKit.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
REVISION=%{release} VERSION=%{version} CGO_ENABLED=1 ./hack/build

%install
install -Dpm 0755 ./bin/build/%{name} %{buildroot}%{plugins_dir}/%{name}

%check
# needs docker, hence kept empty

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{plugins_dir}
%dir %{_libexecdir}/docker
%{plugins_dir}/%{name}

%changelog
* Mon Feb 10 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.17.1-1
- Initial version.
