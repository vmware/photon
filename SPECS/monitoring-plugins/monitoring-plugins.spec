Summary:        Monitoring plugins are used to monitor status of hosts and services on the network
Name:           monitoring-plugins
Version:        2.3.1
Release:        1%{?dist}
License:        GPL-3.0
Group:          Development/Tools
URL:            https://github.com/%{name}
Source0:        https://github.com/%{name}/%{name}/archive/refs/tags/%{name}-%{version}
%define sha1 monitoring-plugins=dbc4c6601c3afe246a13da836d541a315950dde4
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
%setup -q -n %{name}-%{version}
bash tools/setup
%configure

%build
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_prefix}/libexec
%{_prefix}/share/locale/fr
%{_prefix}/share/locale/de


%changelog
* Tue May 11 2021 Sharan Turlapati <sturlapati@vmware.com> 2.3.1-1
- Initial version of monitoring-plugins for Photon
