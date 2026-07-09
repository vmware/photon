%global build_if %{photon_subrelease} >= 91

%global goroot          %{_libdir}/golang
%global gopath          %{_datadir}/gocode
%define debug_package   %{nil}
%define __strip         /bin/true
%define pkg_name        go
%global __requires_exclude_from ^/.*$
%global __provides_exclude_from ^/.*$

%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        Go
Name:           go1.26
Version:        1.26.3
Release:        1%{?dist}
URL:            https://golang.org
License:        BSD
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

%ifarch aarch64
Source0: https://go.dev/dl/%{pkg_name}%{version}.linux-arm64.tar.gz
%define sha512 go=443ebe1f87b426cf21954048d1fee8a122e3f082fb285eae3ef7ba8f793a8efcd5599f46f85777560f38de573011a6dba4a1a6effc457c4367f34d621a66f976
%endif

%ifarch x86_64
Source0: https://go.dev/dl/%{pkg_name}%{version}.linux-amd64.tar.gz
%define sha512 go=cc49ca9764b1dff5983d7635bc6e8f9fe71754bf48ec310a43512cef6103c4a88ed446e9b759742affa9bbcac507957fb9993011cb94343b88ba938c17632c28
%endif

Requires: glibc
Requires: gcc

Conflicts: go

%description
Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.

%prep
%autosetup -p1 -n %{pkg_name}

mkdir -p %{goroot}
test -e bin/go && mv bin %{goroot} || :

%if 0%{?with_check} == 0
find . -type d -name "testdata" -exec rm -rf {} +
%endif

%build
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
export GOROOT_BOOTSTRAP=%{goroot}
export GOROOT="$PWD"
export GOPATH=%{gopath}
export GOROOT_FINAL=%{_bindir}/go

cp -a api doc lib pkg src misc VERSION go.env $GOROOT_BOOTSTRAP

pushd src
bash make.bash -v
popd

%install
mkdir -p %{buildroot}%{_bindir} \
         %{buildroot}%{goroot}

cp -a api bin doc lib pkg src misc VERSION go.env %{buildroot}%{goroot}

# put binaries to bindir, linked to the arch we're building,
# leave the arch independent pieces in %{goroot}
mkdir -p %{buildroot}%{goroot}/bin/linux_%{gohostarch}
ln -sfv ../go %{buildroot}%{goroot}/bin/linux_%{gohostarch}/go
ln -sfv ../gofmt %{buildroot}%{goroot}/bin/linux_%{gohostarch}/gofmt
ln -sfrv %{buildroot}%{goroot}/bin/gofmt %{buildroot}%{_bindir}/gofmt
ln -sfrv %{buildroot}%{goroot}/bin/go %{buildroot}%{_bindir}/go

# ensure these exist and are owned
mkdir -p %{buildroot}%{gopath}/src/github.com/ \
         %{buildroot}%{gopath}/src/bitbucket.org/ \
         %{buildroot}%{gopath}/src/code.google.com/ \
         %{buildroot}%{gopath}/src/code.google.com/p/

install -vdm755 %{buildroot}%{_sysconfdir}/profile.d

cat > %{buildroot}%{_sysconfdir}/profile.d/go-exports.sh <<- "EOF"
export GOROOT=%{goroot}
export GOPATH=%{_datadir}/gocode
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
export GOOS=linux
EOF

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  #This is uninstall
  rm -rf %{_sysconfdir}/profile.d/go-exports.sh \
         /opt/%{pkg_name}
  exit 0
fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%exclude %{goroot}/src/*.rc
%{_sysconfdir}/profile.d/go-exports.sh
%{goroot}/*
%{gopath}/src
%ifarch aarch64
%exclude %dir %{goroot}/src/debug/dwarf/testdata
%exclude %dir %{goroot}/src/debug/elf/testdata
%endif
%{_bindir}/*

%changelog
* Thu Jul 09 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.26.3-1
- Initial version.
- This version of go will help in building newer version of go dependent packages
