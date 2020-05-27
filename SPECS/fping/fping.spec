Summary:       Utility to send ICMP echo probes to network hosts
Name:          fping
Version:       4.1
Release:       1%{?dist}
License:       Charityware
Group:         Productivity/Networking/Diagnostic
Vendor:        VMware, Inc.
Distribution:  Photon
URL:           http://www.fping.org/
Source0:       http://fping.org/dist/%{name}-%{version}.tar.gz
%define sha1 fping=4eda89e12b81d2d0f95919c303286fe1b3667ffe
BuildRequires: autoconf
BuildRequires: automake

%description
fping is a ping like program which uses the Internet Control Message Protocol
(ICMP) echo request to determine if a target host is responding.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
ln -sf fping %{buildroot}%{_sbindir}/fping6
rm -rf %{buildroot}%{_infodir}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%{_sbindir}/fping
%{_sbindir}/fping6
%doc CHANGELOG.md COPYING
%doc %{_mandir}/man8/fping.8*

%changelog
* Wed Jan 23 2019 Dweep Advani <dadvani@vmware.com> 4.1-1
- Added fping package to Photon 2.0
