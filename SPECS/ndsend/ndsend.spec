Summary:       Send unsolicited IPv6 NA packets to refresh neighbor cache.
Name:          ndsend
Version:       1.0.0
Release:       1%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       Public Domain
URL:           https://github.com/blueboxgroup/vzctl
Source0:       %{name}-%{version}.tar.gz
Distribution:  Photon
%define sha1 ndsend=05493e1b8e920959fdf72dc6ab4517504d6ebec3

%description
ndsend is a utility that can send unsolicited IPv6 neighbor advertisement
packets announcing a specified IPv6 address to all IPv6 nodes as per RFC 4861.

%prep
%setup -q

%build
make

%install
make DESTDIR=%{buildroot} install

%post
/sbin/ldconfig

%files
%defattr(-,root,root)
/usr/sbin/ndsend

%changelog
*   Thu Sep 15 2016 Vinay Kulkarni <kulkarniv@vmware.com> 1.0.0-1
-   Initial ndsend utility.
