%global build_if %{photon_subrelease} >= 91
%global debug_package %{nil}

%define srcname     buildx
%define plugins_dir %{_libexecdir}/docker/cli-plugins
%define network_required 1

Name:       docker-buildx
Summary:    Docker CLI plugin for extended build capabilities with BuildKit
Version:    0.32.0
Release:    3%{?dist}
URL:        https://github.com/docker/buildx
Group:      Applications
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/docker/buildx/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: go

Requires: docker

%description
Docker CLI plugin for extended build capabilities with BuildKit.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
# Modeled on deprecated ./hack/build
REVISION=%{release}
VERSION=%{version}
PACKAGE=github.com/docker/buildx
CGO_ENABLED=1
DESTDIR=./bin/build/
GO_PKG=github.com/docker/buildx
GO_LDFLAGS="-X ${GO_PKG}/version.Version=${VERSION} \
  -X ${GO_PKG}/version.Revision=${REVISION} \
  -X ${GO_PKG}/version.Package=${PACKAGE}"

go build \
  -mod vendor \
  -trimpath \
  -ldflags "${GO_LDFLAGS}" \
  -o "${DESTDIR}/docker-buildx" \
  ./cmd/buildx

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
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.32.0-3
- Extended to build for subrelease 91 and above
* Tue Mar 31 2026 Michelle Wang <michelle.wang@broadcom.com> 0.32.0-2
- Disable debuginfo package
* Wed Mar 04 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 0.32.0-1
- Upgrade to 0.32.0, fixes CVE-2025-0495
* Tue Feb 24 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.17.1-6
- Bump up as part of docker upgrade
* Wed Feb 04 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.17.1-5
- Bump version as a part of go upgrade
* Sat Jul 12 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.17.1-4
- Bump version as a part of go upgrade
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.17.1-3
- Release bump for SRP compliance
* Fri Nov 22 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 0.17.1-2
- Bump up as part of docker upgrade
* Sat Oct 12 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.17.1-1
- Initial version.
