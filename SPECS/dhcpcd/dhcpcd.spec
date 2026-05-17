%global build_if %{photon_subrelease} >= 91

Summary:      A minimalistic network configuration daemon with DHCPv4, rdisc and DHCPv6 support
Name:         dhcpcd
Version:      10.2.4
Release:      2%{?dist}
URL:          http://roy.marples.name/projects/%{name}/
Group:        System Environment/Base
Vendor:       VMware, Inc.
Distribution: Photon
Source0:      https://github.com/NetworkConfiguration/dhcpcd/releases/download/v%{version}/%{name}-%{version}.tar.xz
Source1:      %{name}@.service
Source2:      %{name}-sysuser.conf
Source3:      license.txt

%include %{SOURCE3}

BuildRequires: systemd-rpm-macros
BuildRequires: systemd-devel

Requires(pre): shadow
#Obsoletes:     dhcp-client

%description
The dhcpcd package provides a minimalistic network configuration daemon
that supports IPv4 and IPv6 configuration including configuration discovery
through NDP, DHCPv4 and DHCPv6 protocols.

%package      doc
Summary:      Documentation for %{name}
Requires:     %{name} = %{version}-%{release}

%description  doc
%{summary}

%prep
%autosetup -p1 %{name}-%{version}

%build
%configure --dbdir=%{_localstatedir}/lib/%{name} --runstatedir=%{_rundir}
%make_build

%check
%make_build check

%install
export BINMODE=755
%make_install
find %{buildroot} -name '*.la' -delete -print
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}@.service
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf
install -d %{buildroot}%{_sharedstatedir}/%{name}

%pre
%sysusers_create_compat %{SOURCE2}

%files
%defattr(-,root,root,-)
%license LICENSE
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/hooks
%{_datadir}/%{name}/hooks/*
%{_libdir}/%{name}
%{_libexecdir}/%{name}-hooks
%{_libexecdir}/%{name}-run-hooks
%{_sbindir}/%{name}
%{_unitdir}/%{name}@.service
%{_sysusersdir}/%{name}.conf
%defattr(0644,root,dhcpcd,0755)
%{_sharedstatedir}/%{name}

%files doc
%defattr(-,root,root,-)
%{_mandir}/*/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 10.2.4-2
- Extended to build for subrelease 91 and above
* Mon Apr 20 2026 Bo Gan <bo.gan@broadcom.com> 10.2.4-1
- Initial packaging
