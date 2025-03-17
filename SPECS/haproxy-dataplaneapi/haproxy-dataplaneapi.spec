%define network_required 1
%global debug_package   %{nil}
%global repo            https://github.com/haproxytech/dataplaneapi
%global srcname         dataplaneapi
%global commit          891e0ebb8a07fa0babcc31579700021561b4d017
%global build_date      %(date -u '+%Y-%m-%dT%H:%M:%SZ')
%global build_id        %(echo %{build_date} | openssl sha1 | cut -d' ' -f2)

Summary:        A sidecar process for managing HAProxy.
Name:           haproxy-dataplaneapi
Version:        2.7.1
Release:        18%{?dist}
URL:            %{repo}
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/haproxytech/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires: go
BuildRequires: ca-certificates

Requires: haproxy >= 2.0.10

%description
HAProxy Data Plane API is a sidecar process that runs next to HAProxy
and provides API endpoints for managing HAProxy.

%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
CGO_ENABLED=0 \
  go build -trimpath -ldflags "\
    -X main.GitRepo=%{SOURCE0} \
    -X main.GitTag=%{version}-%{release} \
    -X main.GitCommit=%{commit} \
    -X main.GitDirty= \
    -X main.BuildTime=%{build_date} \
    -s -w -B 0x%{build_id} -extldflags=-Wl,-z,now,-z,relro,-z,defs" \
    -o %{srcname} ./cmd/%{srcname}/

%install
install -m 755 -D %{srcname} %{buildroot}%{_libexecdir}/haproxy/%{srcname}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libexecdir}/haproxy/%{srcname}

%changelog
* Wed Mar 05 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.7.1-18
- Spec cleanups
* Fri Jan 10 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.7.1-17
- Fix go input dependencies which have Capital letters in name.
* Wed Jan 08 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.7.1-16
- Release bump for network_required packages
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 2.7.1-15
- Release bump for SRP compliance
* Fri Jul 12 2024 Mukul Sikka <mukul.sikka@broadcom.com> 2.7.1-14
- Bump version as a part of go upgrade
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 2.7.1-13
- Bump version as a part of go upgrade
* Thu Feb 22 2024 Mukul Sikka <msikka@vmware.com> 2.7.1-12
- Bump version as a part of go upgrade
* Thu Dec 14 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.1-11
- Bump up version to compile with new go
* Fri Dec 08 2023 Nitesh Kumar <kunitesh@vmware.com> 2.7.1-10
- Version bump up to use haproxy v2.8.2
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.1-9
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.1-8
- Bump up version to compile with new go
* Mon Aug 21 2023 Nitesh Kumar <kunitesh@vmware.com> 2.7.1-7
- Version bump up to use haproxy v2.7.10
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.1-6
- Bump up version to compile with new go
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.1-5
- Bump up version to compile with new go
* Thu May 18 2023 Nitesh Kumar <kunitesh@vmware.com> 2.7.1-4
- Version bump up to use haproxy v2.7.3
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.1-3
- Bump up version to compile with new go
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.1-2
- Bump up version to compile with new go
* Tue Dec 13 2022 Gerrit Photon <photon-checkins@vmware.com> 2.7.1-1
- Automatic Version Bump
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 2.6.1-2
- Bump up version to compile with new go
* Thu Nov 03 2022 Nitesh Kumar <kunitesh@vmware.com> 2.6.1-1
- Version upgrade to v2.6.1
* Fri Sep 16 2022 Nitesh Kumar <kunitesh@vmware.com> 2.5.4-3
- Version bump up to use haproxy-2.6.4
* Tue Jul 19 2022 Piyush Gupta <gpiyush@vmware.com> 2.5.4-2
- Bump up version to compile with new go
* Sun May 29 2022 Gerrit Photon <photon-checkins@vmware.com> 2.5.4-1
- Automatic Version Bump
* Tue Mar 15 2022 Nitesh Kumar <kunitesh@vmware.com> 2.2.0-2
- Version bump up to use haproxy-2.5.5
* Fri Feb 19 2021 HarinadhD <hdommaraju@vmware.com> 2.2.0-1
- Initial release
