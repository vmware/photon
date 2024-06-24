%global commit          284d34bb4aebf36df8ba1ad430adfd72c222d08b
%global commitdate      20200415
%global version         1.2.5
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global repo            dataplaneapi
%global cmd             %{repo}
%global build_date      %(date '+%%Y-%%m-%%dT%%H:%%M:%%S')
# Required to avoid an error once integrating the Go Build ID.
%global debug_package   %{nil}

Summary:        A sidecar process for managing HAProxy.
Name:           haproxy-%{repo}
Version:        1.2.5
Release:        26%{?dist}
License:        Apache License 2.0
URL:            https://github.com/haproxytech/%{repo}
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/haproxytech/%{repo}-%{version}.tar.gz
%define sha512 %{repo}=46341142e0fda0dde25dc6c4df7fc7abccc8989d7a44f777a0f6fc647d0f9d26761b0602600cde5798d016daa0a6f1034aa9b5343d93c614c14f740a223bda56

BuildRequires: go >= 1.13
BuildRequires: ca-certificates

Requires: haproxy >= 2.0.10

%description
HAProxy Data Plane API is a sidecar process that runs next to HAProxy
and provides API endpoints for managing HAProxy.

%prep
%autosetup -n %{repo}-%{version}

%build
%define gcflags -N -l
# The build_id and ldflags_for_build_id are the solution for the issue
# that the Build ID in Go binaries:
# - the issue       https://github.com/rpm-software-management/rpm/issues/367
# - the work-around https://github.com/aws/amazon-ssm-agent/issues/268
%define build_id %(head -c20 /dev/urandom|od -An -tx1|tr -d '[:space:]')
%define ldflags_for_build_id -s -w -B 0x%{build_id} -extldflags=-Wl,-z,now,-z,relro,-z,defs
%define ldflags_for_build_metadata -X main.GitRepo=%{Source0} -X main.GitTag=v%{version} -X main.GitCommit=%{commit} -X main.GitDirty= -X main.BuildTime=%{build_date}
%define ldflags %{ldflags_for_build_id} %{ldflags_for_build_metadata}
export CGO_ENABLED=0
go build -gcflags "%{gcflags}" -ldflags "%{ldflags}" -o %{cmd} ./cmd/%{cmd}/

%install
install -m 755 -D %{cmd} %{buildroot}%{_libexecdir}/haproxy/%{cmd}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libexecdir}/haproxy/%{cmd}

%changelog
* Mon Jun 24 2024 Mukul Sikka <msikka@vmware.com> 1.2.5-26
- Bump version as a part of go upgrade
* Tue Nov 21 2023 Piyush Gupta <gpiyush@vmware.com> 1.2.5-25
- Bump up version to compile with new go
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.2.5-24
- Bump up version to compile with new go
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 1.2.5-23
- Bump up version to compile with new go
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.2.5-22
- Bump up version to compile with new go
* Wed Jul 26 2023 Nitesh Kumar <kunitesh@vmware.com> 1.2.5-21
- Version bump up to use haproxy v2.2.29
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.2.5-20
- Bump up version to compile with new go
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.2.5-19
- Bump up version to compile with new go
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 1.2.5-18
- Bump up version to compile with new go
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.5-17
- Bump up version to compile with new go
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.5-16
- Bump up version to compile with new go
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.5-15
- Bump up version to compile with new go
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.5-14
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.5-13
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.5-12
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.5-11
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.5-10
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.5-9
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.5-8
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.5-7
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.2.5-6
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.5-5
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.2.5-4
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.2.5-3
- Bump up version to compile with new go
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.2.5-2
- Bump up version to compile with new go
* Mon Apr 20 2020 Andrew Kutz <akutz@vmware.com> 1.2.5-1
- Add haproxy-dataplaneapi v1.2.5 package.
