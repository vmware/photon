Name:           salt3
Version:        3006.7
Release:        3%{?dist}
Summary:        A parallel remote execution system with python3
Group:          System Environment/Daemons
URL:            http://saltstack.org/
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/saltstack/salt/releases/download/v%{version}/salt-%{version}.tar.gz
%define sha512  salt=9d1759a7c0dfc9ad4fdc94460f0f3799483737207bfdc8ddd1424e5c6083ea74ef520f13c323d5cbd7f65c1d9bb13bbbeb5f2cafe6dcacbc2689e733794aef2d
Source2:        salt-master.service
Source3:        salt-syndic.service
Source4:        salt-minion.service
Source5:        salt-api.service
Source6:        logrotate.salt
Source7:        salt-default.preset

Source8: license.txt
%include %{SOURCE8}

Patch0:         requirements.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  systemd
BuildRequires:  python3-distro

Requires:       pciutils
Requires:       python3-backports_abc
Requires:       python3-pycryptodomex
Requires:       python3-jinja2
Requires:       python3-msgpack
Requires:       python3-PyYAML
Requires:       python3-requests
Requires:       python3-zmq
Requires:       python3-tornado
Requires:       python3-psutil
Requires:       python3-distro
Requires:       python3-looseversion
Requires:       python3-jmespath

%ifarch x86_64
Requires:       dmidecode
%endif

%description
Salt is a distributed remote execution system used to execute commands and
query data. It was developed in order to bring the best solutions found in
the world of remote execution together and make them better, faster and more
malleable. Salt accomplishes this via its ability to handle larger loads of
information, and not just dozens, but hundreds or even thousands of individual
servers, handle them quickly and through a simple and manageable interface.

%package        master
Summary:        Management component for salt, a parallel remote execution system with python3
Group:          System Environment/Daemons
Requires:       %{name} = %{version}-%{release}

%description    master
The Salt master is the central server to which all minions connect.

%package        minion
Summary:        Client component for Salt, a parallel remote execution system
Group:          System Environment/Daemons
Requires:       %{name} = %{version}-%{release}

%description    minion
The Salt minion is the agent component of Salt. It listens for instructions
from the master, runs jobs, and returns results back to the master.

%package        syndic
Summary:        Master-of-master component for Salt, a parallel remote execution system
Group:          System Environment/Daemons
Requires:       %{name} = %{version}-%{release}

%description    syndic
The Salt syndic is a master daemon which can receive instruction from a
higher-level master, allowing for tiered organization of your Salt
infrastructure.

%package        api
Summary:        REST API for Salt, a parallel remote execution system
Group:          System administration tools
Requires:       %{name}-master = %{version}-%{release}

%description    api
salt-api provides a REST interface to the Salt master.

%package        cloud
Summary:        Cloud provisioner for Salt, a parallel remote execution system
Group:          System administration tools
Requires:       %{name}-master = %{version}-%{release}

%description    cloud
The salt-cloud tool provisions new cloud VMs, installs salt-minion on them, and
adds them to the master's collection of controllable minions.

%package        ssh
Summary:        Agentless SSH-based version of Salt, a parallel remote execution system
Group:          System administration tools
Requires:       %{name} = %{version}-%{release}

%description    ssh
The salt-ssh tool can run remote execution functions and states without the use
of an agent (salt-minion) service.

%package        proxy
Summary:        Command Proxy of Salt, a parallel remote execution system
Group:          System administration tools
Requires:       %{name} = %{version}-%{release}

%description    proxy
Receives commands from a Salt master and proxies these commands to devices
that are unable to run a full minion.

%package spm
Summary:        Salt Package Manager of Salt, a parallel remote execution system
Group:          System administration tools
Requires:       %{name} = %{version}-%{release}

%description    spm
Salt Package Manager

%prep
%autosetup -n salt-%{version} -p1

%build

%install
cd %{_builddir}/salt-%{version}
python3 setup.py install -O1 --root %{buildroot}

# Add some directories
install -d -m 0755 %{buildroot}%{_var}/cache/salt
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.conf.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.deploy.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.maps.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.profiles.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/cloud.providers.d

# Add the config files
install -p -m 0640 conf/minion %{buildroot}%{_sysconfdir}/salt/minion
install -p -m 0640 conf/master %{buildroot}%{_sysconfdir}/salt/master
install -p -m 0640 conf/cloud %{buildroot}%{_sysconfdir}/salt/cloud
install -p -m 0640 conf/roster %{buildroot}%{_sysconfdir}/salt/roster

mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE4} %{buildroot}%{_unitdir}/
install -p -m 0644 %{SOURCE5} %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -p -m 0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/salt

install -v -D -m 0644 %{SOURCE7} %{buildroot}%{_presetdir}/50-salt.preset

%clean
rm -rf %{buildroot}

%preun master
%systemd_preun salt-master.service

%preun syndic
%systemd_preun salt-syndic.service

%preun minion
%systemd_preun salt-minion.service

%post master
%systemd_post salt-master.service

%post minion
%systemd_post salt-minion.service

%postun master
%systemd_postun salt-master.service

%postun syndic
%systemd_postun salt-syndic.service

%postun minion
%systemd_postun salt-minion.service

%files
%defattr(-,root,root,-)
%{python3_sitelib}/salt/*
%{python3_sitelib}/salt-*-py3.11.egg-info
%{_sysconfdir}/logrotate.d/salt
%{_var}/cache/salt
%{_bindir}/salt-pip
%{_presetdir}/50-salt.preset

%files master
%defattr(-,root,root)
%doc %{_mandir}/man7/salt.7.*
%doc %{_mandir}/man1/salt-cp.1.*
%doc %{_mandir}/man1/salt-key.1.*
%doc %{_mandir}/man1/salt-master.1.*
%doc %{_mandir}/man1/salt-run.1.*
%doc %{_mandir}/man1/salt.1.*
%{_bindir}/salt
%{_bindir}/salt-cp
%{_bindir}/salt-key
%{_bindir}/salt-master
%{_bindir}/salt-run
%{_unitdir}/salt-master.service
%config(noreplace) %{_sysconfdir}/salt/master

%files minion
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-call.1.*
%doc %{_mandir}/man1/salt-minion.1.*
%{_bindir}/salt-minion
%{_bindir}/salt-call
%{_unitdir}/salt-minion.service
%config(noreplace) %{_sysconfdir}/salt/minion

%files syndic
%defattr(-,root,root,-)
%doc %{_mandir}/man1/salt-syndic.1.*
%{_bindir}/salt-syndic
%{_unitdir}/salt-syndic.service

%files api
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-api.1.*
%{_bindir}/salt-api
%{_unitdir}/salt-api.service

%files cloud
%defattr(-,root,root,-)
%doc %{_mandir}/man1/salt-cloud.1.*
%{_bindir}/salt-cloud
%{_sysconfdir}/salt/cloud.conf.d
%{_sysconfdir}/salt/cloud.deploy.d
%{_sysconfdir}/salt/cloud.maps.d
%{_sysconfdir}/salt/cloud.profiles.d
%{_sysconfdir}/salt/cloud.providers.d
%config(noreplace) %{_sysconfdir}/salt/cloud

%files ssh
%defattr(-,root,root,-)
%doc %{_mandir}/man1/salt-ssh.1.*
%{_bindir}/salt-ssh
%{_sysconfdir}/salt/roster

%files proxy
%defattr(-,root,root,-)
%doc %{_mandir}/man1/salt-proxy.1.*
%{_bindir}/salt-proxy

%files spm
%defattr(-,root,root,-)
%doc %{_mandir}/man1/spm.1.*
%{_bindir}/spm

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 3006.7-3
- Release bump for SRP compliance
* Mon May 13 2024 Etienne Le Sueur <etienne.le-sueur@broadcom.com> 3006.7-2
- Update requirements to include python3-jmespath to fix issue listing minions
* Wed Apr 17 2024 Prafful Mehrotra <prafful.mehrotra@broadcom.com> 3006.7-1
- Update to 3006.7-1 for Ph5 and adding python_backport_abc, looseversion
