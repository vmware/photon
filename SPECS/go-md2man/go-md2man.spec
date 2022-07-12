%define gopath_comp github.com/cpuguy83/go-md2man
Summary:        Converts markdown into roff (man pages)
Name:           go-md2man
Version:        2.0.0
Release:        11%{?dist}
License:        MIT
URL:            https://github.com/cpuguy83/go-md2man
Source0:        https://github.com/cpuguy83/go-md2man/archive/%{name}-%{version}.tar.gz
%define sha512  go-md2man=22a6c950ca7e386246fadb15f05d0a60437a249df48a7c5f905bc4bd05034cede6318e1158bd2113e97b4fd2d1e838776680a00c6141ac2b3c8795aeee15a39d
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go >= 1.11
BuildRequires:  which

%description
Converts markdown into roff (man pages).

%prep
%autosetup -c
mkdir -p "$(dirname "src/%{gopath_comp}")"
mv %{name}-%{version} src/%{gopath_comp}

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
* Tue Jul 12 2022 Piyush Gupta <gpiyush@vmware.com> 2.0.0-11
- Bump up version to compile with new go
*   Sat May 07 2022 Piyush Gupta <gpiyush@vmware.com> 2.0.0-10
-   Bump up version to compile with new go
*   Tue Feb 22 2022 Piyush Gupta <gpiyush@vmware.com> 2.0.0-9
-   Bump up version to compile with new go
*   Mon Jan 24 2022 Piyush Gupta <gpiyush@vmware.com> 2.0.0-8
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 2.0.0-7
-   Bump up version to compile with new go
*   Tue Oct 05 2021 Piyush Gupta <gpiyush@vmware.com> 2.0.0-6
-   Bump up version to compile with new go
*   Fri Jun 11 2021 Piyush Gupta <gpiyush@vmware.com> 2.0.0-5
-   Bump up version to compile with new go
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 2.0.0-4
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 2.0.0-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 2.0.0-2
-   Bump up version to compile with new go
*   Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.0-1
-   Initial packaging for go-md2man for containerd
