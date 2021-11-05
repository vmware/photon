%global goroot          /usr/lib/golang
%global gopath          %{_datadir}/gocode
%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif
%define debug_package %{nil}
%define __strip /bin/true

# rpmbuild magic to keep from having meta dependency on libc.so.6
#%define _use_internal_dependency_generator 0
#%define __find_requires %{nil}

Summary:        Go
Name:           go
Version:        1.17.2
Release:        1%{?dist}
License:        BSD
URL:            https://golang.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://golang.org/dl/%{name}%{version}.src.tar.gz
%define sha1    go=b78350fa6e4617c1eac66dff656eda8df0a13c1f
Requires:       glibc
%define ExtraBuildRequires go

%description
Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.

%prep
%autosetup -p1 -n %{name}

%build
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
export GOROOT_BOOTSTRAP=%{goroot}

export GOROOT="`pwd`"
export GOPATH=%{gopath}
export GOROOT_FINAL=%{_bindir}/go
rm -f  %{gopath}/src/runtime/*.c
pushd src
./make.bash --no-clean
popd

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{goroot}

cp -R api bin doc lib pkg src misc VERSION %{buildroot}%{goroot}

# remove the unnecessary zoneinfo file (Go will always use the system one first)
rm -rfv %{buildroot}%{goroot}/lib/time

# remove the doc Makefile
rm -rfv %{buildroot}%{goroot}/doc/Makefile

# put binaries to bindir, linked to the arch we're building,
# leave the arch independent pieces in %{goroot}
mkdir -p %{buildroot}%{goroot}/bin/linux_%{gohostarch}
ln -sfv ../go %{buildroot}%{goroot}/bin/linux_%{gohostarch}/go
ln -sfv ../gofmt %{buildroot}%{goroot}/bin/linux_%{gohostarch}/gofmt
ln -sfv %{goroot}/bin/gofmt %{buildroot}%{_bindir}/gofmt
ln -sfv %{goroot}/bin/go %{buildroot}%{_bindir}/go

# ensure these exist and are owned
mkdir -p %{buildroot}%{gopath}/src/github.com/
mkdir -p %{buildroot}%{gopath}/src/bitbucket.org/
mkdir -p %{buildroot}%{gopath}/src/code.google.com/
mkdir -p %{buildroot}%{gopath}/src/code.google.com/p/
install -vdm755 %{buildroot}/etc/profile.d
cat >> %{buildroot}/etc/profile.d/go-exports.sh <<- "EOF"
export GOROOT=%{goroot}
export GOPATH=%{_datadir}/gocode
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
export GOOS=linux
EOF
#chown -R root:root %{buildroot}/etc/profile.d/go-exports.sh
#%{_fixperms} %{buildroot}/*

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  #This is uninstall
  rm /etc/profile.d/go-exports.sh
  rm -rf /opt/%{name}
  exit 0
fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%exclude %{goroot}/src/*.rc
%exclude %{goroot}/include/plan9
/etc/profile.d/go-exports.sh
%{goroot}/*
%{gopath}/src
%exclude %{goroot}/src/pkg/debug/dwarf/testdata
%exclude %{goroot}/src/pkg/debug/elf/testdata
%{_bindir}/*

%changelog
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.17.2-1
-   Upgrade to 1.17.2
*   Sat Aug 21 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.7-1
-   Upgrade to 1.16.7
*   Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.2-2
-   Fix for CVE-2021-31525.
*   Mon May 03 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.2-1
-   Update to 1.16.2
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.13.15-3
-   Fix CVE-2020-28367,CVE-2020-28366
*   Wed Nov 25 2020 Harinadh D <hdommaraju@vmware.com> 1.13.15-2
-   Fix CVE-2020-28367,CVE-2020-28366
*   Thu Sep 10 2020 Ashwin H <ashwinh@vmware.com> 1.13.15-1
-   Update to 1.13.15
*   Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 1.13.3-3
-   Fix CVE-2020-16845
*   Fri Apr 10 2020 Harinadh D<hdommaraju@vmware.com> 1.13.3-2
-   Fix for CVE-2020-7919
*   Tue Oct 22 2019 <ashwinh@vmware.com> 1.13.3-1
-   Update to 1.13.3
*   Wed Sep 11 2019 <ashwinh@vmware.com> 1.13-1
-   Initial build for 1.13
