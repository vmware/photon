Summary:        Converts markdown into roff (man pages)
Name:           go-md2man
Version:        2.0.0
Release:        9%{?dist}
License:        MIT
URL:            https://github.com/cpuguy83/go-md2man
Source0:        https://github.com/cpuguy83/go-md2man/archive/%{name}-%{version}.tar.gz
%define sha1    go-md2man=9eb4d8cc03734ff7f470147a6512a5c66d57ccaf

%define gopath_comp github.com/cpuguy83/go-md2man
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
*   Tue Nov 16 2021 Piyush Gupta <gpiyush@vmware.com> 2.0.0-9
-   Bump up version to compile with new go
*   Wed Oct 20 2021 Piyush Gupta <gpiyush@vmware.com> 2.0.0-8
-   Bump up version to compile with new go
*   Sat Aug 21 2021 Piyush Gupta<gpiyush@vmware.com> 2.0.0-7
-   Bump up version to compile with new go
*   Tue Jun 29 2021 Piyush Gupta <gpiyush@vmware.com> 2.0.0-6
-   Bump up version to compile with new go
*   Mon May 03 2021 Piyush Gupta<gpiyush@vmware.com> 2.0.0-5
-   Bump up version to compile with new go
*   Mon Feb 08 2021 Harinadh D <hdommaraju@vmware.com> 2.0.0-4
-   Bump up version to compile with new go
*   Fri Nov 27 2020 HarinadhD <hdommaraju@vmware.com> 2.0.0-3
-   Bump up version to compile with new go
*   Fri Apr 10 2020 Harinadh D <hdommaraju@vmware.com> 2.0.0-2
-   Bump up version to compile with go 1.13.3-2
*   Tue Oct 22 2019 Bo Gan <ganb@vmware.com> 2.0.0-1
-   Initial packaging for go-md2man
