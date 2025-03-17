Summary:        Monitoring plugins are used to monitor status of hosts and services on the network
Name:           monitoring-plugins
Version:        2.3.5
Release:        1%{?dist}
Group:          Development/Tools
URL:            https://github.com/%{name}
Source0:        https://github.com/%{name}/%{name}/archive/refs/tags/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  m4
BuildRequires:  which
BuildRequires:  net-snmp-perl
BuildRequires:  lm-sensors
Requires:       net-snmp-perl

%description
Monitoring plugins maintains a bundle of more than 50 standard plugins.
Typically, the monitoring software runs these plugins to determine the
current status of hosts and services on your network. Each plugin is a
stand alone command line tool that provides a specific type to check.

%prep
%autosetup -n %{name}-%{version}
bash tools/setup
%configure

%build
make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_prefix}/libexec
%{_prefix}/share/locale/fr
%{_prefix}/share/locale/de

%changelog
* Fri Mar 21 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 2.3.5-1
- Update to 2.3.5
- Enchance config.yaml
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 2.3.1-3
- Release bump for SRP compliance
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 2.3.1-2
- Rebuild for perl version upgrade to 5.36.0
* Tue May 11 2021 Sharan Turlapati <sturlapati@vmware.com> 2.3.1-1
- Initial version of monitoring-plugins for Photon
