%global include_tests 1

%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python3_sitearch: %global python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?pythonpath: %global pythonpath %(python3 -c "import os, sys; print(os.pathsep.join(x for x in sys.path if x))")}

%define _salttesting SaltTesting
%define _salttesting_ver 2016.5.11

Name: salt3
Version: 2019.2.8
Release: 3%{?dist}
Summary: A parallel remote execution system with python3
Group:   System Environment/Daemons
License: ASL 2.0
URL:     http://saltstack.org/
Vendor:         VMware, Inc.
Distribution:   Photon
Source0: https://files.pythonhosted.org/packages/0c/6f/c8394676b59948978f80815cdfc5e89b4eaf808f23e9dac8011d04f7d486/salt-%{version}.tar.gz
%define sha1 salt=2bb0fc68e862c3f7e0f2be54c052db4fec11471d
Source1: https://pypi.python.org/packages/source/S/SaltTesting/SaltTesting-2016.5.11.tar.gz
%define sha1 SaltTesting=474dbd7029e3d48cdb468be3c63b2262e47556c8
Source2: salt-master.service
Source3: salt-syndic.service
Source4: salt-minion.service
Source5: salt-api.service
Source6: logrotate.salt
Patch1:  patches_2021_01_28_2019.2.5.patch
Patch2:  patches_2021_02_05_2019.2.5.patch


BuildRoot: %{_tmppath}/salt-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
%ifarch %{ix86} x86_64
Requires: dmidecode
%endif


Requires: pciutils
Requires: python3-backports_abc
BuildRequires: python3-devel
BuildRequires: systemd
Requires: python3-pycryptodomex
Requires: python3-jinja2
Requires: python3-msgpack
Requires: python3-PyYAML
Requires: python3-requests
Requires: python3-zmq
Requires: python3-tornado

%description
Salt is a distributed remote execution system used to execute commands and
query data. It was developed in order to bring the best solutions found in
the world of remote execution together and make them better, faster and more
malleable. Salt accomplishes this via its ability to handle larger loads of
information, and not just dozens, but hundreds or even thousands of individual
servers, handle them quickly and through a simple and manageable interface.

%package master
Summary: Management component for salt, a parallel remote execution system with python3
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}
%description master
The Salt master is the central server to which all minions connect.

%package minion
Summary: Client component for Salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}
%description minion
The Salt minion is the agent component of Salt. It listens for instructions
from the master, runs jobs, and returns results back to the master.

%package syndic
Summary: Master-of-master component for Salt, a parallel remote execution system
Group:   System Environment/Daemons
Requires: %{name} = %{version}-%{release}
%description syndic
The Salt syndic is a master daemon which can receive instruction from a
higher-level master, allowing for tiered organization of your Salt
infrastructure.

%package api
Summary: REST API for Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name}-master = %{version}-%{release}
%description api
salt-api provides a REST interface to the Salt master.

%package cloud
Summary: Cloud provisioner for Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name}-master = %{version}-%{release}
%description cloud
The salt-cloud tool provisions new cloud VMs, installs salt-minion on them, and
adds them to the master's collection of controllable minions.

%package ssh
Summary: Agentless SSH-based version of Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name} = %{version}-%{release}
%description ssh
The salt-ssh tool can run remote execution functions and states without the use
of an agent (salt-minion) service.

%package proxy
Summary: Command Proxy of Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name} = %{version}-%{release}
%description proxy
Receives commands from a Salt master and proxies these commands to devices
that are unable to run a full minion.

%package spm
Summary: Salt Package Manager of Salt, a parallel remote execution system
Group:   System administration tools
Requires: %{name} = %{version}-%{release}
%description spm
Salt Package Manager


%prep
%setup -c -n salt-%{version}
cd salt-%{version}
%patch1 -p1
%patch2 -p1

%build

%install
rm -rf %{buildroot}
cd $RPM_BUILD_DIR/salt-%{version}/salt-%{version}
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

%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc $RPM_BUILD_DIR/salt-%{version}/salt-%{version}/LICENSE
%{python3_sitelib}/salt/*
%{python3_sitelib}/salt-*-py?.?.egg-info
%{_sysconfdir}/logrotate.d/salt
%{_var}/cache/salt


%files master
%defattr(-,root,root)
%doc %{_mandir}/man7/salt.7.*
%doc %{_mandir}/man1/salt-cp.1.*
%doc %{_mandir}/man1/salt-key.1.*
%doc %{_mandir}/man1/salt-master.1.*
%doc %{_mandir}/man1/salt-run.1.*
%doc %{_mandir}/man1/salt-unity.1.*
%doc %{_mandir}/man1/salt.1.*
%{_bindir}/salt
%{_bindir}/salt-cp
%{_bindir}/salt-key
%{_bindir}/salt-master
%{_bindir}/salt-run
%{_bindir}/salt-unity
%config(noreplace) %{_unitdir}/salt-master.service
%config(noreplace) %{_sysconfdir}/salt/master

%files minion
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-call.1.*
%doc %{_mandir}/man1/salt-minion.1.*
%{_bindir}/salt-minion
%{_bindir}/salt-call
%config(noreplace) %{_unitdir}/salt-minion.service
%config(noreplace) %{_sysconfdir}/salt/minion

%files syndic
%doc %{_mandir}/man1/salt-syndic.1.*
%{_bindir}/salt-syndic
%config(noreplace) %{_unitdir}/salt-syndic.service

%files api
%defattr(-,root,root)
%doc %{_mandir}/man1/salt-api.1.*
%{_bindir}/salt-api
%config(noreplace) %{_unitdir}/salt-api.service

%files cloud
%doc %{_mandir}/man1/salt-cloud.1.*
%{_bindir}/salt-cloud
%{_sysconfdir}/salt/cloud.conf.d
%{_sysconfdir}/salt/cloud.deploy.d
%{_sysconfdir}/salt/cloud.maps.d
%{_sysconfdir}/salt/cloud.profiles.d
%{_sysconfdir}/salt/cloud.providers.d
%config(noreplace) %{_sysconfdir}/salt/cloud

%files ssh
%doc %{_mandir}/man1/salt-ssh.1.*
%{_bindir}/salt-ssh
%{_sysconfdir}/salt/roster

%files proxy
%doc %{_mandir}/man1/salt-proxy.1.*
%{_bindir}/salt-proxy

%files spm
%doc %{_mandir}/man1/spm.1.*
%{_bindir}/spm

%preun master
%if 0%{?systemd_preun:1}
  %systemd_preun salt-master.service
%else
  if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable salt-master.service > /dev/null 2>&1 || :
    /bin/systemctl stop salt-master.service > /dev/null 2>&1 || :
  fi

%preun syndic
%if 0%{?systemd_preun:1}
  %systemd_preun salt-syndic.service
%else
  if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable salt-syndic.service > /dev/null 2>&1 || :
    /bin/systemctl stop salt-syndic.service > /dev/null 2>&1 || :
  fi
%endif

%preun minion
%if 0%{?systemd_preun:1}
  %systemd_preun salt-minion.service
%else
  if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable salt-minion.service > /dev/null 2>&1 || :
    /bin/systemctl stop salt-minion.service > /dev/null 2>&1 || :
  fi
%endif

%post master
%if 0%{?systemd_post:1}
  %systemd_post salt-master.service
%else
  /bin/systemctl daemon-reload &>/dev/null || :
%endif

%post minion
%if 0%{?systemd_post:1}
  %systemd_post salt-minion.service
%else
  /bin/systemctl daemon-reload &>/dev/null || :
%endif

%postun master
%if 0%{?systemd_post:1}
  %systemd_postun salt-master.service
%else
  /bin/systemctl daemon-reload &>/dev/null
  [ $1 -gt 0 ] && /bin/systemctl try-restart salt-master.service &>/dev/null || :
%endif

%postun syndic
%if 0%{?systemd_post:1}
  %systemd_postun salt-syndic.service
%else
  /bin/systemctl daemon-reload &>/dev/null
  [ $1 -gt 0 ] && /bin/systemctl try-restart salt-syndic.service &>/dev/null || :
%endif

%postun minion
%if 0%{?systemd_post:1}
  %systemd_postun salt-minion.service
%else
  /bin/systemctl daemon-reload &>/dev/null
  [ $1 -gt 0 ] && /bin/systemctl try-restart salt-minion.service &>/dev/null || :
%endif
%endif

%changelog
* Fri Feb 19 2021 Keerthana K <keerthanak@vmware.com> 2019.2.8-3
- Fix CVE-2020-28243 CVE-2020-28972 CVE-2020-35662 CVE-2021-3148
- CVE-2021-3144 CVE-2021-25281 CVE-2021-25282 CVE-2021-25283
- CVE-2021-25284 CVE-2021-3197
* Tue Jan 19 2021 Tapas Kundu <tkundu@vmware.com> 2019.2.8-2
- Depends on pycrptodomex instead of pycrypto
* Thu Dec 17 2020 Siju Maliakkal <smaliakkal@vmware.com> 2019.2.8-1
- Upgrade to 2019.2.8
* Fri Nov 06 2020 Keerthana K <keerthanak@vmware.com> 2019.2.7-1
- Update to version 2019.2.7
* Tue May 12 2020 Keerthana K <keerthanak@vmware.com> 2019.2.4-1
- Update to version 2019.2.4 to fix CVE-2020-11651 CVE-2020-11652.
* Fri Dec 13 2019 Vinothkumar D <vinothkumard@vmware.com> 2019.2.0-1
- Upgrade to version 2019.2.0.
* Mon Jan 21 2019 Vinothkumar D <vinothkumard@vmware.com> 2018.3.2-1
- Downgrade to version 2018.3.2.
* Tue Dec 04 2018 Vinothkumar D <vinothkumard@vmware.com> 2018.3.3-1
- This is an initial version of salt with python3 support for Photon OS
  The source is from https://github.com/saltstack/salt/archive/v2018.3.3.tar.gz
