%global goroot          /usr/lib/golang
%global gopath          %{_datadir}/gocode
%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif
%define debug_package %{nil}
%define __strip /bin/true
# To disable rpm requires on libc.so
%define _use_internal_dependency_generator 0
%define __find_requires %{nil}

Summary:        Go
Name:           go
Version:        1.20.2
Release:        1%{?dist}
License:        BSD
URL:            https://golang.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://golang.org/dl/%{name}%{version}.src.tar.gz
%define sha512  go=ba8f894b1baa6b3c1bdaafa113feff8d16c25d91f8e44bd4e7ffb46d7b329309290f27385804399baa9834691290a209fc7a193b24fd197ea11a16ce4a1b9d39
Requires:       glibc
Requires:       gcc

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

mkdir -p %{buildroot}%{_bindir} %{buildroot}%{goroot}

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
mkdir -p %{buildroot}%{gopath}/src/github.com/ \
         %{buildroot}%{gopath}/src/bitbucket.org/ \
         %{buildroot}%{gopath}/src/code.google.com/ \
         %{buildroot}%{gopath}/src/code.google.com/p/

install -vdm755 %{buildroot}%{_sysconfdir}/profile.d
cat >> %{buildroot}%{_sysconfdir}/profile.d/go-exports.sh <<- "EOF"
export GOROOT=%{goroot}
export GOPATH=%{_datadir}/gocode
export GOHOSTOS=linux
export GOHOSTARCH=%{gohostarch}
export GOOS=linux
EOF

#chown -R root:root %{buildroot}%{_sysconfdir}/profile.d/go-exports.sh
#%%{_fixperms} %{buildroot}/*

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  #This is uninstall
  rm -rf %{_sysconfdir}/profile.d/go-exports.sh \
         /opt/%{name}
  exit 0
fi

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%exclude %{goroot}/src/*.rc
%exclude %dir %{goroot}/include/plan9
%{_sysconfdir}/profile.d/go-exports.sh
%{goroot}/*
%{gopath}/src
%exclude %dir %{goroot}/src/pkg/debug/dwarf/testdata
%exclude %dir %{goroot}/src/pkg/debug/elf/testdata
%ifarch aarch64
%exclude %dir %{goroot}/src/debug/dwarf/testdata
%exclude %dir %{goroot}/src/debug/elf/testdata
%endif
%{_bindir}/*

%changelog
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.20.2-1
- Upgrade to 1.20.2
* Fri Jan 20 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.19.3-2
- Remove requires on libc.so.6
* Mon Nov 21 2022 Piyush Gupta <gpiyush@vmware.com> 1.19.3-1
- Upgrade to 1.19.3
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.19.2-1
- Upgrade to 1.19.2
* Fri Jun 17 2022 Piyush Gupta <gpiyush@vmware.com> 1.19-1
- Upgrade to 1.19
* Mon Feb 28 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.16.5-2
- Fix binary path
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.5-1
- Update to 1.16.5
* Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 1.15.8-1
- Update to 1.15.8
* Fri Jan 15 2021 Piyush Gupta <gpiyush@vmware.com> 1.15.6-1
- Update to 1.15.6
* Wed Oct 28 2020 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.14.8-2
- Fix glibc dependency on aarch64
* Tue Oct 06 2020 Ashwin H <ashwinh@vmware.com> 1.14.8-1
- Update to 1.14.8
* Thu Mar 05 2020 <ashwinh@vmware.com> 1.14-1
- Initial build for 1.14
