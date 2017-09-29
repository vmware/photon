# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

Name:           traceroute
Summary:        Traces the route taken by packets over an IPv4/IPv6 network
Version:        2.0.22
Release:        2%{?dist}
License:        GPLv2
Group:          Applications/Internet
Url:            http://traceroute.sourceforge.net
Source0:        http://downloads.sourceforge.net/project/traceroute/traceroute/traceroute-%{version}/traceroute-%{version}.tar.gz
%define sha1 traceroute=2d2797a2684fc41639f80537cefabe9a8c27fa7b
Vendor:		VMware, Inc.
Distribution:	Photon


%description
The traceroute utility displays the route used by IP packets on their
way to a specified network (or Internet) host.

%prep
%setup -q


%build
make %{?_smp_mflags}

%install

install -d %{buildroot}/bin
install -m755 traceroute/traceroute %{buildroot}/bin
pushd %{buildroot}/bin
ln -s traceroute traceroute6
popd

install -d %{buildroot}%{_bindir}
install -m755 wrappers/tcptraceroute %{buildroot}%{_bindir}

install -d %{buildroot}%{_mandir}/man8
install -p -m644 traceroute/traceroute.8 %{buildroot}%{_mandir}/man8
pushd %{buildroot}%{_mandir}/man8
ln -s traceroute.8 traceroute6.8
ln -s traceroute.8 tcptraceroute.8
popd


%files
%doc COPYING README TODO CREDITS
/bin/*
%{_bindir}/*
%{_mandir}/*/*


%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.22-2
-	GA - Bump release of all rpms
* 	Fri Feb 26 2016 Anish Swaminathan <anishs@vmware.com>  2.0.22-1
- 	Initial version
