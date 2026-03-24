%global build_if %{photon_subrelease} >= 92

Summary:        IPv6 diagnostic tools
Name:           ndisc6
Version:        1.0.8
Release:        1%{?dist}
URL:            https://www.remlab.net/ndisc6/
Group:          Applications/Internet
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.remlab.net/files/%{name}/%{name}-%{version}.tar.bz2

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  gettext
BuildRequires:  perl

Requires:       glibc
Requires:       perl

%description
NDisc6 is a small collection of useful tools for IPv6 networking.

%package        docs
Summary:        Documentation for ndisc6
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description    docs
The package contains ndisc6 documentation files such as
AUTHORS, NEWS, MAN pages and README.

%prep
%autosetup

%build
%configure --disable-suid-install
%make_build

%install
%make_install
%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%config(noreplace) %{_sysconfdir}/rdnssd/
%{_bindir}/addr2name
%{_bindir}/dnssort
%{_bindir}/name2addr
%{_sbindir}/ndisc6
%{_sbindir}/rdisc6
%{_sbindir}/rltraceroute6
%{_bindir}/tcpspray
%{_bindir}/tcpspray6
%{_sbindir}/tcptraceroute6
%{_sbindir}/tracert6
%{_sbindir}/rdnssd

%files docs
%defattr(-,root,root)
%doc AUTHORS NEWS README
%{_mandir}/man1/addr2name.1*
%{_mandir}/man1/dnssort.1*
%{_mandir}/man1/name2addr.1*
%{_mandir}/man1/tcpspray.1*
%{_mandir}/man1/tcpspray6.1*
%{_mandir}/man8/ndisc6.8*
%{_mandir}/man8/rdisc6.8*
%{_mandir}/man8/rdnssd.8*
%{_mandir}/man8/rltraceroute6.8*
%{_mandir}/man8/tcptraceroute6.8*
%{_mandir}/man8/tracert6.8*

%changelog
* Tue Mar 24 2026 Mukul Sikka <mukul.sikka@broadcom.com> 1.0.8-1
- Initial build.
