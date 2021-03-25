Summary:        confd is a lightweight configuration management tool
Name:           confd
Version:        3.16
Release:        4%{?dist}
License:        Apache-2.0
URL:            https://github.com/projectcalico/confd
Source0:        %{name}-%{version}.tar.gz
%define sha1 confd=2df9721bb22364ce2f8c565a10780865c4f70221
Source1:        vendor-%{name}-%{version}.tar.gz
%define sha1 vendor-%{name}-%{version}.tar.gz=070ee0bac01696cd342cd12e099f88f9dab8bbd4
Obsoletes:       calico-confd
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  go
BuildRequires:  tar

%description
This is a Calico-specific version of confd. It is heavily modified from the original and only supports a single backend type - namely a Calico datastore. It has a single purpose which is to monitor Calico BGP configuration and to autogenerate bird BGP templates from that config.

%prep
%setup -n %{name}-release-v%{version}

%build
tar -zxf %{SOURCE1}
mkdir -p dist
go build -v -i -o dist/confd confd.go

%install
install -vdm 755 %{buildroot}/%{_bindir}/confd
install -vpm 0755 -t %{buildroot}/%{_bindir}/confd dist/confd
cp -r etc/ %{buildroot}%{_sysconfdir}

%files
%defattr(-,root,root)
%{_bindir}/confd/confd
%config(noreplace) %{_sysconfdir}/calico

%changelog
*   Thu Mar 25 2021 Piyush Gupta<gpiyush@vmware.com> 3.16-4
-   Bump up version to compile with new go
*   Fri Feb 05 2021 Harinadh D <hdommaraju@vmware.com> 3.16-3
-   Bump up version to compile with new go
*   Fri Jan 15 2021 Piyush Gupta<gpiyush@vmware.com> 3.16-2
-   Bump up version to compile with new go
*   Tue Oct 13 2020 Ashwin H <ashwinh@vmware.com> 3.16-1
-   Update to 3.16
*   Wed Jun 17 2020 Ashwin H <ashwinh@vmware.com> 3.6-3
-   Fix dependency for cloud.google.com-go
*   Tue Jun 09 2020 Ashwin H <ashwinh@vmware.com> 3.6-2
-   Use cache for dependencies
*   Fri Aug 16 2019 Ashwin H <ashwinh@vmware.com> 3.6-1
-   project calico-confd initial version
