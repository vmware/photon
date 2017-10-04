Summary:       BGP implementation in Go
Name:          gobgp
Version:       1.23
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Apache-2.0
URL:           https://github.com/osrg/gobgp
Source0:       gosrc-gobgp.txt
Source1:       deps-gobgp.txt
Distribution:  Photon
BuildRequires: git
BuildRequires: go >= 1.7
%define debug_package %{nil}

%description
GoBGP is an open source BGP implementation designed from scratch for modern environment and implemented in a modern programming language, the Go Programming Language.

%prep
%gosrc_prep

%build
export GOPATH="`pwd`"; export PATH="$GOPATH/bin:$PATH";

# restore golang/dep and gobgp source
cd src
%with_git_mirror %gosrc_restore %{SOURCE0}

%with_git_mirror go get github.com/golang/dep/cmd/dep
# This go get will report no buildable Go source,
# which is the correct behavior of gobgp
%with_git_mirror go get github.com/osrg/gobgp || :

cd github.com/osrg/gobgp
%with_git_mirror dep ensure
pushd gobgpd && go install && popd
pushd gobgp && go install && popd

#check sources and deps
cd vendor
%with_git_mirror %gosrc_verify_no_vendor %{SOURCE1}
cd "${GOPATH}/src"
%with_git_mirror %gosrc_verify_no_vendor %{SOURCE0}

%install
install -vdm 755 %{buildroot}%{_bindir}
install bin/gobgp %{buildroot}%{_bindir}/
install bin/gobgpd %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%{_bindir}/gobgp
%{_bindir}/gobgpd
%doc src/github.com/osrg/gobgp/LICENSE
%doc src/github.com/osrg/gobgp/README.md

%changelog
*    Fri Oct 06 2017 Bo Gan <ganb@vmware.com> 1.23-2
-    Use gosrc for source tracking
*    Mon Sep 11 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.23-1
-    Go BGP daemon for PhotonOS.
