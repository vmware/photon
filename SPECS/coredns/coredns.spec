%ifarch aarch64
%global gohostarch      arm64
%else
%global gohostarch      amd64
%endif

Summary:        CoreDNS
Name:           coredns
Version:        1.7.1
Release:        1%{?dist}
License:        Apache License 2.0
URL:            https://github.com/coredns/coredns/releases/v%{version}.tar.gz
Source0:        coredns-%{version}.tar.gz
%define sha512  coredns=4ac92d040afb145d0b721ba381704741d2e0eb32f0f7e53788195fb72c06bcd7c915ac698396d5f7c27df899c7f526045e39d08cb37ae04d2ca871930d299ac0
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  git
%define debug_package %{nil}

%description
CoreDNS is a DNS server that chains plugins

%prep -p exit
%autosetup -n coredns-%{version}

%build
export ARCH=%{gohostarch}
export VERSION=%{version}
export PKG=github.com/%{name}/%{name}
export GOARCH=${ARCH}
export GOHOSTARCH=${ARCH}
export GOOS=linux
export GOHOSTOS=linux
export GOROOT=/usr/lib/golang
export GOPATH=/usr/share/gocode
export GOBIN=/usr/share/gocode/bin
export PATH=$PATH:$GOBIN
export GO111MODULE=auto
mkdir -p ${GOPATH}/src/${PKG}
cp -rf . ${GOPATH}/src/${PKG}
pushd ${GOPATH}/src/${PKG}
# Just download (do not compile), since it's not compilable with go-1.9.
# TODO: use prefetched tarball instead.
sed -i 's#go get -u github.com/mholt/caddy#go get -u -d github.com/mholt/caddy#' Makefile
sed -i 's#go get -u github.com/miekg/dns#go get -u -d github.com/miekg/dns#' Makefile
make %{?_smp_mflags}

%install
install -m 755 -d %{buildroot}%{_bindir}
install -pm 755 -t %{buildroot}%{_bindir} ${GOPATH}/src/github.com/%{name}/%{name}/coredns

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/coredns

%changelog
* Wed Oct 26 2022 Piyush Gupta <gpiyush@vmware.com> 1.7.1-1
- Upgraded to 1.7.1.
* Thu Sep 15 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.0-20
- Bump up version to compile with new go
* Thu Aug 18 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.0-19
- Bump up version to compile with new go
* Mon May 09 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.0-18
- Bump up version to compile with new go
* Wed Mar 16 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.0-17
- Bump up version to compile with new go
* Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.0-16
- Bump up version to compile with new go
* Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 1.2.0-15
- Bump up version to compile with new go
* Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.0-14
- Bump up version to compile with new go
* Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.0-13
- Bump up version to compile with new go
* Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 1.2.0-12
- Bump up version to compile with new go
* Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 1.2.0-11
- Bump up version to compile with new go
* Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 1.2.0-10
- Bump up version to compile with new go
* Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 1.2.0-9
- Bump up version to compile with new go
* Thu Dec 17 2020 Ankit Jain <ankitja@vmware.com> 1.2.0-8
- Repo changed from github.com/mholt/caddy to github.com/caddyserver/caddy
* Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 1.2.0-7
- Bump up version to compile with new go
* Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 1.2.0-6
- Bump up version to compile with go 1.13.3-2
* Tue Oct 22 2019 Ashwin H <ashwinh@vmware.com> 1.2.0-5
- Bump up version to compile with go 1.13.3
* Sun Sep 22 2019 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-4
- Fix compilation issue (do not compile mholt/caddy).
* Fri Aug 30 2019 Ashwin H <ashwinh@vmware.com> 1.2.0-3
- Bump up version to compile with new go
* Sun Sep 23 2018 Alexey Makhalov <amakhalov@vmware.com> 1.2.0-2
- Fix compilation issue.
- aarch64 support.
* Fri Aug 03 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.2.0-1
- Initial version of coredns 1.2.0.
