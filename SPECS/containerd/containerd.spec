%define debug_package %{nil}
Summary:        Containerd
Name:           containerd
Version:        1.2.8
Release:        2%{?dist}
License:        ASL 2.0
URL:            https://containerd.io/docs/
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/containerd/containerd/archive/containerd-%{version}.tar.gz
%define sha1 containerd=57f84e241a1344c5c6cc3884b41bcfe3fd614d57

BuildRequires:  runc
BuildRequires:  btrfs-progs
BuildRequires:  btrfs-progs-devel
BuildRequires:  libseccomp
BuildRequires:  libseccomp-devel
BuildRequires:  go >= 1.10.7
BuildRequires:  git
Requires:       libseccomp

%description
Containerd is an open source project. It is available as a daemon for Linux,
which manages the complete container lifecycle of its host system.

%package        doc
Summary:        containerd
Requires:       %{name} = %{version}

%description    doc
Documentation for containerd.

%prep
%setup -q -c

%build
export PKG=github.com/containerd
export GOPATH=/usr/share/gocode
export GOROOT=/usr/lib/golang
export GOHOSTOS=linux
export CGO_ENABLED=0
export GOOS=linux
export VERSION=%{version}
mkdir -p ${GOPATH}/src/${PKG}
cp -r * ${GOPATH}/src/${PKG}/.
pushd ${GOPATH}/src/${PKG}/%{name}
make BUILDTAGS=no_btrfs
popd

%install
export PKG=github.com/containerd
export GOPATH=/usr/share/gocode
export GOROOT=/usr/lib/golang
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_mandir}
mkdir -p %{buildroot}%{_docdir}/%{name}
pushd ${GOPATH}/src/${PKG}/%{name}
make install
cp -r ./bin/* %{buildroot}%{_bindir}
cp -r ./*.md %{buildroot}%{_docdir}/%{name}
cp -r ./docs/* %{buildroot}%{_docdir}/%{name}
popd

%check
export PKG=github.com/containerd
export GOPATH=/usr/share/gocode
export GOROOT=/usr/lib/golang
export GOHOSTOS=linux
export CGO_ENABLED=1
export GOOS=linux
mkdir -p ${GOPATH}/src/${PKG}
pushd ${GOPATH}/src/${PKG}/%{name}
make test
make root-test
make integration
popd

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*

%files doc
%defattr(-,root,root)
%{_docdir}/*

%changelog
*   Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.2.8-2
-   Bump up version to compile with go 1.13.3
*   Tue Aug 27 2019 Shreyas B. <shreyasb@vmware.com> 1.2.8-1
-   Initial version of containerd spec.
