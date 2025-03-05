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
Release:        13%{?dist}
License:        Apache License 2.0
URL:            %{repo}
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/haproxytech/%{name}-%{version}.tar.gz
%define sha512 %{name}=f534e6a6622e09cfe505201317f9a6237df6bf347758b844c92266fb9606d493fc43bdb11f6bd16e63372caf1fb3642c6c944805a5c1e7e5791433b64a73dacc

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
* Wed Mar 05 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.7.1-13
- Spec cleanups
* Thu Dec 14 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.1-12
- Bump up version to compile with new go
* Fri Dec 08 2023 Nitesh Kumar <kunitesh@vmware.com> 2.7.1-11
- Version bump up to use haproxy v2.8.2
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.1-10
- Bump up version to compile with new go
* Mon Sep 18 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.1-9
- Bump up version to compile with new go
* Thu Sep 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.7.1-8
- Fix a source0 mishap while building
* Mon Aug 21 2023 Nitesh Kumar <kunitesh@vmware.com> 2.7.1-7
- Version bump up to use haproxy v2.7.10
* Mon Jul 17 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.1-6
- Bump up version to compile with new go
* Mon Jul 03 2023 Piyush Gupta <gpiyush@vmware.com> 2.7.1-5
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
