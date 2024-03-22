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
#%%define _use_internal_dependency_generator 0
#%%define __find_requires %{nil}

Summary:        Go
Name:           go
Version:        1.20.12
Release:        2%{?dist}
License:        BSD
URL:            https://golang.org
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://golang.org/dl/%{name}%{version}.src.tar.gz
%define sha512  go=3f4d1a22a0f1dd7e8feb008517e43b32c3600ce77168e5edfb75b4060577362ae62f28c9891de0f7bf553407bd8e09efc1563d34ee8af5285b3c80b3946f4b65
Requires:       glibc

Patch0:         CVE-2023-45288.patch

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
#%%{_fixperms} %{buildroot}/*

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
* Fri Mar 22 2024 Mukul Sikka <msikka@vmware.com> 1.20.12-2
- Fix for CVE-2023-45288
* Fri Dec 15 2023 Mukul Sikka <msikka@vmware.com> 1.20.12-1
- Upgrade to 1.20.12
* Wed Oct 11 2023 Piyush Gupta <gpiyush@vmware.com> 1.20.10-1
- Upgrade to 1.20.10
* Tue Sep 26 2023 Piyush Gupta <gpiyush@vmware.com> 1.20.8-1
- Upgrade to 1.20.8
* Fri Aug 18 2023 Piyush Gupta <gpiyush@vmware.com> 1.20.7-1
- Upgrade to 1.20.7
* Thu Jun 22 2023 Piyush Gupta <gpiyush@vmware.com> 1.20.5-1
- Upgrade to 1.20.5
* Wed May 03 2023 Piyush Gupta <gpiyush@vmware.com> 1.20.4-1
- Upgrade to 1.20.4.
* Tue Apr 04 2023 Piyush Gupta <gpiyush@vmware.com> 1.20.2-1
- Upgrade to 1.20.2.
* Tue Dec 20 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.8-2
- Fix for CVE-2022-41717.
* Sun Nov 13 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.8-1
- Upgrade to 1.18.8.
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.7-1
- Upgrade to 1.18.7.
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.6-1
- Upgrade to 1.18.6.
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.5-1
- Upgrade to 1.18.5.
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.18.1-1
- Upgrade to 1.18.1.
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.17.2-5
- Fix for CVE-2022-24921.
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.17.2-4
- Fix for CVE-2022-23806 and CVE-2022-23772, CVE-2022-23773.
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.17.2-3
- Fix for CVE-2021-44716 and CVE-2021-44717.
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.17.2-2
- Fix for CVE-2021-41771, CVE-2021-41772.
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.17.2-1
- Upgrade to 1.17.2
* Sat Aug 21 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.7-1
- Upgrade to 1.16.7
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.2-2
- Fix for CVE-2021-31525.
* Mon May 03 2021 Piyush Gupta <gpiyush@vmware.com> 1.16.2-1
- Update to 1.16.2
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.13.15-3
- Fix CVE-2020-28367,CVE-2020-28366
* Wed Nov 25 2020 Harinadh D <hdommaraju@vmware.com> 1.13.15-2
- Fix CVE-2020-28367,CVE-2020-28366
* Thu Sep 10 2020 Ashwin H <ashwinh@vmware.com> 1.13.15-1
- Update to 1.13.15
* Tue Aug 18 2020 Ashwin H <ashwinh@vmware.com> 1.13.3-3
- Fix CVE-2020-16845
* Fri Apr 10 2020 Harinadh D<hdommaraju@vmware.com> 1.13.3-2
- Fix for CVE-2020-7919
* Tue Oct 22 2019 <ashwinh@vmware.com> 1.13.3-1
- Update to 1.13.3
* Wed Sep 11 2019 <ashwinh@vmware.com> 1.13-1
- Initial build for 1.13
