Summary:        CLI tool for spawning and running containers per OCI spec.
Name:           runc
Version:        0.1.1
Release:        3%{?dist}
License:        ASL 2.0
URL:            https://runc.io/
Source0:        https://github.com/opencontainers/runc/archive/%{name}-v%{version}.tar.gz
%define sha1    runc=ca70c97c9211462f774e22f03fec2fe61f45f1ba
Patch0:         CVE-2019-5736.patch
Group:          Virtualization/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  curl
BuildRequires:  gawk
BuildRequires:  go
BuildRequires:  iptables-devel
BuildRequires:  pkg-config
BuildRequires:  libaio-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-c-devel
BuildRequires:  python2-devel
Requires:       glibc
Requires:       libgcc
Requires:       libseccomp

%description
runC is a CLI tool for spawning and running containers according to the OCI specification. Containers are started as a child process of runC and can be embedded into various other systems without having to run a daemon.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
make %{?_smp_mflags}

%install
install -D -m0755 runc %{buildroot}%{_sbindir}/runc

%files
%defattr(-,root,root)
%{_sbindir}/runc

%changelog
*   Mon Feb 11 2019 Bo Gan <ganb@vmware.com> 0.1.1-3
-   Fix CVE-2019-5736
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.1-2
-   Add iptables-devel to BuildRequires
*   Tue Apr 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.1.1-1
-   Initial runc package for PhotonOS.
