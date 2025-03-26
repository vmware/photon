%define srcname     buildx
%define plugins_dir %{_libexecdir}/docker/cli-plugins

Name:       docker-buildx
Summary:    Docker CLI plugin for extended build capabilities with BuildKit
Version:    0.17.1
Release:    3%{?dist}
URL:        https://github.com/docker/buildx
Group:      Applications
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/docker/buildx/archive/refs/tags/%{srcname}-%{version}.tar.gz

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
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.17.1-3
- Release bump for SRP compliance
* Fri Nov 22 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.17.1-2
- Bump up as part of docker upgrade
* Sat Oct 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.17.1-1
- Initial version.
