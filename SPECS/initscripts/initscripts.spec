Summary:	Scripts to bring up network interfaces and legacy utilities
Name:		initscripts
Version:	10.04
License:	GPLv2
Group:		System Environment/Base
Release:	1%{?dist}
URL:		https://github.com/fedora-sysv/initscripts
Source0:	https://github.com/fedora-sysv/initscripts/archive/%{name}-%{version}.tar.gz
%define sha1 initscripts=b9e707441d4be947cd1c75c3733671900cfa11df
Source1:        adjtime
Patch0:         service.patch
Vendor:     	VMware, Inc.
Distribution:   Photon
Requires:	systemd
Requires:	iproute2
Requires:       util-linux
Requires:       findutils
BuildRequires:	glib-devel
BuildRequires:	python3
BuildRequires:	python3-libs
BuildRequires:	popt-devel
BuildRequires:	gettext
BuildRequires:	pkg-config
BuildRequires:	systemd
Provides:	/sbin/service

%description
This package contains the script that activates and deactivates most
network interfaces, some utilities, and other legacy files.

%package -n netconsole-service
Summary:          Service for initializing of network console logging
Requires:         %{name} = %{version}-%{release}
BuildArch:        noarch

Requires:         iputils
Requires:         kmod
Requires:         sed

%description -n netconsole-service
This packages provides a 'netconsole' service for loading of netconsole kernel
module with the configured parameters. The netconsole kernel module itself then
allows logging of kernel messages over the network.

%package -n readonly-root
Summary:          Service for configuring read-only root support
Requires:         %{name} = %{version}-%{release}
BuildArch:        noarch

Requires:         cpio

%description -n readonly-root
This package provides script & configuration file for setting up read-only root
support. Additional configuration is required after installation.

%prep
%setup -q
%patch0 -p1

%build
make PYTHON=/usr/bin/python3

%install
%make_install

%find_lang %{name}

%ifnarch s390 s390x
rm -f \
  %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-ctc \
%endif

# Additional ways to access documentation:
install -m 0755 -d %{buildroot}%{_docdir}/network-scripts

ln -s  %{_docdir}/%{name}/sysconfig.txt %{buildroot}%{_docdir}/network-scripts/
ln -sr %{_mandir}/man8/ifup.8           %{buildroot}%{_mandir}/man8/ifdown.8

cp -r %{SOURCE1} %{buildroot}%{_sysconfdir}/

mkdir -p %{buildroot}%{_sysconfdir}/rwtab.d
mkdir -p %{buildroot}%{_sysconfdir}/statetab.d

mkdir -p %{buildroot}%{_sysconfdir}/NetworkManager/dispatcher.d

cat >> %{buildroot}%{_sysconfdir}/sysconfig/network <<- "EOF"
###
# This file is used to specify information about the desired network configuration.
# By default, it contains the following options:
#

# A boolean yes or no to Configure networking or not to configure networking.
# NETWORKING=boolean

# Hostname of your machine
# HOSTNAME=value

# where gwip is the IP address of the remote network gateway -if available.
# GATEWAY=gwip
EOF

cat >> %{buildroot}%{_sysconfdir}/networks <<- "EOF"
default 0.0.0.0
loopback 127.0.0.0
link-local 169.254.0.0
EOF

%post
%systemd_post import-state.service loadmodules.service

%preun
%systemd_preun import-state.service loadmodules.service

%postun
%systemd_postun import-state.service loadmodules.service

%post -n netconsole-service
%systemd_post netconsole.service

%preun -n netconsole-service
%systemd_preun netconsole.service

%postun -n netconsole-service
%systemd_postun netconsole.service

%post -n readonly-root
%systemd_post readonly-root.service

%preun -n readonly-root
%systemd_preun readonly-root.service

%postun -n readonly-root
%systemd_postun readonly-root.service

%files -f %{name}.lang
%license COPYING
%doc doc/sysconfig.txt

# NOTE: /etc/sysconfig/ is owned by filesystem package.
%dir %{_sysconfdir}/rc.d
%dir %{_sysconfdir}/rc.d/init.d
%dir %{_sysconfdir}/rc.d/rc[0-6].d
%dir %{_sysconfdir}/sysconfig/modules
%dir %{_libexecdir}/%{name}
%dir %{_libexecdir}/%{name}/legacy-actions
%exclude %{_sysconfdir}/sysconfig/console
%{_sysconfdir}/rc.d/init.d/functions

# RC symlinks:
%{_sysconfdir}/rc[0-6].d
%{_sysconfdir}/init.d

%{_bindir}/*
%{_sbindir}/consoletype
%{_sbindir}/genhostid
%{_sbindir}/service
%{_libexecdir}/import-state
%{_libexecdir}/loadmodules
%{_prefix}/lib/systemd/system/import-state.service
%{_prefix}/lib/systemd/system/loadmodules.service
%{_prefix}/lib/udev/rename_device
%{_udevrulesdir}/*
%{_mandir}/man1/*
%{_mandir}/man8/service.*

# network-scripts
%doc doc/examples/
%dir %{_sysconfdir}/sysconfig/network-scripts
%{_sysconfdir}/rc.d/init.d/network
%{_sysconfdir}/sysconfig/network-scripts/*
%config(noreplace)    %{_sysconfdir}/sysconfig/network-scripts/ifcfg-lo
%ifarch s390 s390x
%{_sysconfdir}/sysconfig/network-scripts/ifup-ctc
%endif
%config(noreplace) %{_sysconfdir}/sysconfig/network
%config(noreplace) %{_sysconfdir}/networks
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/adjtime

%attr(4755,root,root) %{_sbindir}/usernetctl
%{_mandir}/man8/ifup.*
%{_mandir}/man8/ifdown.*
%{_mandir}/man8/usernetctl.*
%{_docdir}/network-scripts/*

%dir %{_sysconfdir}/NetworkManager
%dir %{_sysconfdir}/NetworkManager/dispatcher.d

%files -n netconsole-service
%config(noreplace) %{_sysconfdir}/sysconfig/netconsole
%{_libexecdir}/netconsole
%{_prefix}/lib/systemd/system/netconsole.service

%files -n readonly-root
%dir %{_sharedstatedir}/stateless
%dir %{_sharedstatedir}/stateless/state
%dir %{_sharedstatedir}/stateless/writable
%dir %{_sysconfdir}/rwtab.d
%dir %{_sysconfdir}/statetab.d
%config(noreplace) %{_sysconfdir}/rwtab
%config(noreplace) %{_sysconfdir}/statetab
%config(noreplace) %{_sysconfdir}/sysconfig/readonly-root
%{_libexecdir}/readonly-root
%{_prefix}/lib/systemd/system/readonly-root.service

%changelog
*   Wed Jul 22 2020 Ankit Jain <ankitja@vmware.com> 10.04-1
-   Updated to 10.04
*   Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 9.70-4
-   Build using python3
*   Sat Jan 05 2019 Ankit Jain <ankitja@vmware.com> 9.70-3
-   Added network configuration to fix "service --status-all"
*   Tue Dec 26 2017 Divya Thaluru <dthaluru@vmware.com> 9.70-2
-   Fixed return code in /etc/init.d/functions bash script
*   Mon Apr 3 2017 Dheeraj Shetty <dheerajs@vmware.com> 9.70-1
-   Updated to version 9.70
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.65-2
-   GA - Bump release of all rpms
*   Fri Feb 12 2016 Divya Thaluru <dthaluru@vmware.com> 9.65-2
-   Fixing service script to start services using systemctl by default
*   Tue Jan 26 2016 Xiaolin Li <xiaolinl@vmware.com> 9.65-1
-   Updated to version 9.65
*   Mon Jul 20 2015 Divya Thaluru <dthaluru@vmware.com> 9.63-1
-   Got Spec file from source tar ball and modified it to be compatible to build in Photon
