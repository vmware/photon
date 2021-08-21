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
Release:        6%{?dist}
License:        Apache License 2.0
URL:            https://github.com/haproxytech/%{repo}
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/haproxytech/%{repo}-%{version}.tar.gz
%define sha1    %{repo}=9cfca3f7b240a51bb6e5995350a377aa6d7054f2
BuildRequires:  go >= 1.13
BuildRequires:  ca-certificates
Requires:       haproxy >= 2.0.10

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
*   Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.2.5-6
-   Bump up version to compile with new go
*   Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.5-5
-   Bump up version to compile with new go
*   Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.2.5-4
-   Bump up version to compile with new go
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.2.5-3
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.2.5-2
-   Bump up version to compile with new go
*   Mon Apr 20 2020 Andrew Kutz <akutz@vmware.com> 1.2.5-1
-   Add haproxy-dataplaneapi v1.2.5 package.
