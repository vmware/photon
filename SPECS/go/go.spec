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
Version:        1.21.13
Release:        1%{?dist}
License:        BSD
URL:            https://golang.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://golang.org/dl/%{name}%{version}.src.tar.gz
%define sha512  %{name}=f316984154ead8256d9ec0613e3cfef5699553387d87c24bb2a96265f986bf4450838e6451841def3713d65ebaa9bf55e36ff39c5690d79522e1c1ba7655be2f

Requires:       glibc
Requires:       gcc

Patch1: CVE-2024-34156.patch
Patch2: CVE-2024-34158.patch

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

cp -R api bin doc lib pkg src misc VERSION go.env %{buildroot}%{goroot}

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
* Thu Sep 19 2024 Mukul Sikka <msikka@vmware.com> 1.21.13-1
- Upgrade to 1.21.13
- Fix CVE-2024-34156 and CVE-2024-34158
* Fri Jul 12 2024 Mukul Sikka <msikka@vmware.com> 1.21.12-1
- Upgrade to 1.21.12
* Thu Jun 20 2024 Mukul Sikka <msikka@vmware.com> 1.21.11-1
- Upgrade to 1.21.11
* Thu Apr 18 2024 Mukul Sikka <msikka@vmware.com> 1.21.7-1
- Upgrade to 1.21.7
* Fri Mar 22 2024 Mukul Sikka <msikka@vmware.com> 1.20.12-2
- Fix for CVE-2023-45288
* Fri Dec 15 2023 Mukul Sikka <msikka@vmware.com> 1.20.12-1
- Upgrade to 1.20.12
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.20.10-1
- Upgrade to 1.20.10
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.20.8-1
- Upgrade to 1.20.8
* Tue Jun 20 2023 Piyush Gupta <gpiyush@vmware.com> 1.20.5-1
- Upgrade to 1.20.5
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.20.4-1
- Upgrade to 1.20.4
* Thu Mar 09 2023 Piyush Gupta <gpiyush@vmware.com> 1.20.2-1
- Upgrade to 1.20.2
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.19.3-2
- Fix for CVE-2022-41717.
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.19.3-1
- Upgrade to 1.19.3.
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.19.2-1
- Upgrade to 1.19.2.
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.19.1-1
- Upgrade to 1.19.1.
* Fri Aug 19 2022 Piyush Gupta <gpiyush@vmware.com> 1.19-1
- Upgrade to 1.19.
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.1-2
- Fix for CVE-2022-29526.
* Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.1-1
- Upgrade to 1.18.1.
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.17.2-3
- Fix for CVE-2022-23806, CVE-2022-23772, CVE-2022-23773.
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.17.2-2
- Fix for CVE-2021-44716, CVE-2021-44717.
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.17.2-1
- Upgrade to 1.17.2
* Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.7-1
- Upgrade to 1.16.7
* Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.5-1
- Update to 1.16.5
* Thu Mar 25 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.2-1
- Update to 1.16.2
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
