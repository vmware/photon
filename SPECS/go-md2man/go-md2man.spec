%define gopath_comp github.com/cpuguy83/go-md2man
Summary:        Converts markdown into roff (man pages)
Name:           go-md2man
Version:        2.0.1
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/cpuguy83/go-md2man
Source0:        https://github.com/cpuguy83/go-md2man/archive/%{name}-%{version}.tar.gz
%define sha512    go-md2man=293141da791cddd56e9b92d936cbd6105675e8c1ebf6fa95e79a3651ff28d050596b31d48256414e2a8e70d8054ee163885808635b8bb029ec49f5f81678d390
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go >= 1.11
BuildRequires:  which

%description
Converts markdown into roff (man pages).

%prep
%autosetup
cd ../
mkdir -p "$(dirname "src/%{gopath_comp}")"
mkdir -p src/%{gopath_comp}
mv %{name}-%{version}/* src/%{gopath_comp}/
mv src %{name}-%{version}/

%build
export GOPATH="$(pwd)"
cd src/%{gopath_comp}
# Disable GO Modules for now. go.mod has extraneous entries
make %{?_smp_mflags} GO111MODULE=off

%install
cd src/%{gopath_comp}
install -v -m755 -D -t %{buildroot}%{_bindir} bin/go-md2man
install -v -m644 -D -t %{buildroot}%{_docdir}/licenses/%{name} LICENSE.md

%files
%defattr(-,root,root)
%{_bindir}/go-md2man
%{_docdir}/licenses/%{name}

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.1-1
-   Automatic Version Bump
*   Fri Jun 11 2021 Piyush Gupta<gpiyush@vmware.com> 2.0.0-4
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 2.0.0-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 2.0.0-2
-   Bump up version to compile with new go
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.0-1
-   Initial packaging for go-md2man for containerd
