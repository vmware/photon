Name:           vmware-lightwave-clients
Summary:        VMware Infrastructure Client
Version:        1.2.0
Release:        1%{?dist}
License:        Apache 2.0
Group:          Applications/System
Vendor:         VMware, Inc.
URL: 	        https://github.com/vmware/lightwave
Distribution:   Photon

Requires:  coreutils >= 8.22
Requires:  openssl >= 1.0.2
Requires:  likewise-open >= 6.2.11
Requires:  vmware-directory-client = %{version}
Requires:  vmware-afd = %{version}
Requires:  vmware-ca-client = %{version}
Requires:  vmware-ic-config = %{version}
Requires:  vmware-dns-client = %{version}

%description
VMware Infrastructure Controller Clients

%prep

%build

%files
%defattr(-,root,root,0755)

%changelog
*   Thu Mar 30 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-1
-   Initial - spec modified for Photon from lightwave git repo.
