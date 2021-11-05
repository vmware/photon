%define debug_package %{nil}

Summary:        CRI tools
Name:           cri-tools
Version:        1.17.0
Release:        8%{?dist}
License:        Apache License Version 2.0
URL:            https://github.com/kubernetes-incubator/cri-tools/archive/%{name}-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1    %{name}-%{version}.tar.gz=5343b85c2b8df9ce1f90f80d043d7323afcec2b6
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go

%description
cri-tools aims to provide a series of debugging and validation tools for Kubelet CRI, which includes:
crictl: CLI for kubelet CRI.
critest: validation test suites for kubelet CRI.

%prep
%autosetup

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/lib/.build-id
mkdir -p %{buildroot}/usr/share/doc/cri-tools
mkdir -p %{buildroot}/usr/share/licenses/cri-tools
mkdir -p %{buildroot}/man/man1

%make_install
cp /usr/local/bin/crictl %{buildroot}/usr/bin
cp /usr/local/bin/critest %{buildroot}/usr/bin
cp CHANGELOG.md %{buildroot}/usr/share/doc/cri-tools
cp LICENSE %{buildroot}/usr/share/licenses/cri-tools
cp CHANGELOG.md %{buildroot}/usr/share/doc/cri-tools
cp CONTRIBUTING.md %{buildroot}/usr/share/doc/cri-tools
cp OWNERS %{buildroot}/usr/share/doc/cri-tools
cp README.md %{buildroot}/usr/share/doc/cri-tools
cp code-of-conduct.md %{buildroot}/usr/share/doc/cri-tools
cp docs/validation.md %{buildroot}/usr/share/doc/cri-tools
cp docs/roadmap.md %{buildroot}/usr/share/doc/cri-tools

%files
%defattr(-,root,root)
%{_datadir}/%{name}
/usr/bin
/usr/share/doc/*
/usr/share/licenses/*
/man/man1/

%clean
rm -rf %{buildroot}/*

%changelog
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.17.0-8
-   Bump up version to compile with new go
*   Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.17.0-7
-   Bump up version to compile with new go
*   Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.17.0-6
-   Bump up version to compile with new go
*   Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.17.0-5
-   Bump up version to compile with new go
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.17.0-4
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.17.0-3
-   Bump up version to compile with new go
*   Wed Apr 22 2020 Harinadh D <hdommaraju@vmware.com> 1.17.0-2
-   Bump up version to compile with go 1.13.3-2
*   Wed Apr 15 2020 Ashwin H <ashwinh@vmware.com> 1.17.0-1
-   Update to 1.17.0
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.11.1-3
-   Bump up version to compile with go 1.13.3
*   Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.11.1-2
-   Bump up version to compile with new go
*    Thu Jul 26 2018 Tapas Kundu <tkundu@vmware.com> 1.11.1-1
-    Initial build added for Photon.
