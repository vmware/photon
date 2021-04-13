%define debug_package %{nil}

Summary:        CRI tools
Name:           cri-tools
Version:        1.21.0
Release:        1%{?dist}
License:        Apache License Version 2.0
URL:            https://github.com/kubernetes-incubator/cri-tools/archive/%{name}-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1    %{name}-%{version}.tar.gz=ebc09c9effed6534ff2a48054f35fd16b7e3a526
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  git

%description
cri-tools aims to provide a series of debugging and validation tools for Kubelet CRI, which includes:
crictl: CLI for kubelet CRI.
critest: validation test suites for kubelet CRI.

%prep
%setup -qn %{name}-%{version}

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

make install DESTDIR=%{buildroot}
cp build/bin/crictl %{buildroot}/usr/bin
cp build/bin/critest %{buildroot}/usr/bin
cp CHANGELOG.md %{buildroot}/usr/share/doc/cri-tools
cp LICENSE %{buildroot}/usr/share/licenses/cri-tools
cp CHANGELOG.md %{buildroot}/usr/share/doc/cri-tools
cp CONTRIBUTING.md %{buildroot}/usr/share/doc/cri-tools
cp OWNERS %{buildroot}/usr/share/doc/cri-tools
cp README.md %{buildroot}/usr/share/doc/cri-tools
cp code-of-conduct.md %{buildroot}/usr/share/doc/cri-tools
cp docs/validation.md %{buildroot}/usr/share/doc/cri-tools
cp docs/roadmap.md %{buildroot}/usr/share/doc/cri-tools
rm %{buildroot}/usr/local/bin/crictl
rm %{buildroot}/usr/local/bin/critest

%files
%defattr(-,root,root)
%{_datadir}/%{name}
%{_bindir}/crictl
%{_bindir}/critest
%{_datadir}/doc/*
%{_datadir}/licenses/*
/man/man1/

%clean
rm -rf %{buildroot}/*

%changelog
*   Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 1.21.0-1
-   Automatic Version Bump
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.19.0-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 1.19.0-2
-   Bump up version to compile with new go
*    Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 1.19.0-1
-    Automatic Version Bump
*    Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.18.0-1
-    Automatic Version Bump
*    Thu Jul 26 2018 Tapas Kundu <tkundu@vmware.com> 1.11.1-1
-    Initial build added for Photon.
