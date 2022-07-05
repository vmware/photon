%global commit          68bd22b2219d043e2f4f982ff8aa03262888a277
%global commitdate      20210115
%global version         2.2.0
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global repo            dataplaneapi
%global cmd             %{repo}
%global build_date      %(date '+%%Y-%%m-%%dT%%H:%%M:%%S')
# Required to avoid an error once integrating the Go Build ID.
%global debug_package   %{nil}

Summary:        A sidecar process for managing HAProxy.
Name:           haproxy-%{repo}
Version:        2.2.0
Release:        2%{?dist}
License:        Apache License 2.0
URL:            https://github.com/haproxytech/%{repo}
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/haproxytech/%{repo}-%{version}.tar.gz
%define sha1    %{repo}=d4ce27bfb1bc564b87ab98362c87e0ee1a2919b0
BuildRequires:  go
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
*   Tue Mar 15 2022 Nitesh Kumar <kunitesh@vmware.com> 2.2.0-2
-   Version bump up to use haproxy-2.5.5
*   Fri Feb 19 2021 HarinadhD <hdommaraju@vmware.com> 2.2.0-1
-   Initial release
