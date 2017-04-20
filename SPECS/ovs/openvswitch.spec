Summary:        Open vSwitch daemon/database/utilities
Name:           openvswitch
Version:        2.7.0
Release:        1%{?dist}
License:        ASL 2.0 and LGPLv2+
URL:            http://www.openvswitch.org/
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://openvswitch.org/releases/%{name}-%{version}.tar.gz
%define sha1 openvswitch=0f324ccfe52ae84a2b102a7f2db1411f4debacf6

BuildRequires:  gcc >= 4.0.0
BuildRequires:  libcap-ng
BuildRequires:  libcap-ng-devel
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  python2 >= 2.7.0
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-pip
BuildRequires:  python-six
BuildRequires:  python-xml
BuildRequires:  python-setuptools

Requires:       libgcc-atomic
Requires:       libcap-ng
Requires:       openssl
Requires:       PyYAML
Requires:       python2
Requires:       python2-libs
Requires:       python-xml
Requires:       python-configobj
Requires:       python-jsonpatch
Requires:       python-prettytable
Requires:       python-requests

%description
Open vSwitch provides standard network bridging functions and
support for the OpenFlow protocol for remote per-flow control of
traffic.

%package	devel
Summary:	Header and development files for openvswitch
Requires:	%{name} = %{version}
%description    devel
openvswitch-devel package contains header files and libs.

%package        doc
Summary:        Documentation for openvswitch
Requires:       %{name} = %{version}-%{release}
%description    doc
It contains the documentation and manpages for openvswitch.

%prep
%setup -q

%build
./configure \
        CFLAGS="%{optflags}" \
        --prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --libdir=%{_libdir} \
        --sysconfdir=/etc \
        --localstatedir=/var \
        --enable-ssl \
        --enable-shared \
        --disable-static

make %{_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete

mkdir -p %{buildroot}/%{_libdir}/systemd/system
cat << EOF >> %{buildroot}/%{_libdir}/systemd/system/openvswitch.service
[Unit]
Description=Open vSwitch

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/usr/bin/mkdir -p /etc/openvswitch
ExecStartPre=/usr/bin/mkdir -p /var/run/openvswitch
ExecStartPre=/sbin/modprobe openvswitch
ExecStartPre=/usr/bin/bash -c "[ -f /etc/openvswitch/conf.db ] || ovsdb-tool create /etc/openvswitch/conf.db /usr/share/openvswitch/vswitch.ovsschema"
ExecStart=/usr/bin/bash -c "[[ -n \$(pidof ovsdb-server) ]] || ovsdb-server --remote=punix:/var/run/openvswitch/db.sock --remote=db:Open_vSwitch,Open_vSwitch,manager_options --pidfile --detach"
ExecStart=/usr/bin/ovs-vsctl --no-wait init
ExecStart=/usr/bin/bash -c "[[ -n \$(pidof ovs-vswitchd) ]] || ovs-vswitchd --pidfile --detach"
ExecStop=/usr/bin/bash -c "[ -f /var/run/openvswitch/ovs-vswitchd.pid ] && kill \$(cat /var/run/openvswitch/ovs-vswitchd.pid)"
ExecStop=/usr/bin/bash -c "[ -f /var/run/openvswitch/ovsdb-server.pid ] && kill \$(cat /var/run/openvswitch/ovsdb-server.pid)"
ExecStopPost=/sbin/modprobe -r openvswitch

[Install]
WantedBy=multi-user.target
EOF

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

#TODO: Make a systemctl file to start and stop OVS

%files
%defattr(-,root,root)
%{_bindir}/ovs-*
%{_bindir}/ovsdb-*
%{_bindir}/ovn-*
%{_bindir}/vtep-ctl
%{_sbindir}/ovs-*
%{_sbindir}/ovsdb-server
%{_libdir}/systemd/system/openvswitch.service
%{_libdir}/lib*
%{_sysconfdir}/bash_completion.d/ovs-*-bashcomp.bash
%{_datadir}/openvswitch/*.ovsschema
%{_datadir}/openvswitch/bugtool-plugins/*
%{_datadir}/openvswitch/python/*
%{_datadir}/openvswitch/scripts/ovs-*
%{_datadir}/openvswitch/scripts/ovn-*
%{_datadir}/openvswitch/scripts/ovndb-servers.ocf

%files devel
%{_includedir}/ovn/*.h
%{_includedir}/openflow/*.h
%{_includedir}/openvswitch/*.h
%{_libdir}/pkgconfig/*.pc

%files doc
%{_mandir}/man1/ovs-*.1.gz
%{_mandir}/man1/ovsdb-*.1.gz
%{_mandir}/man5/ovs-vswitchd.conf.db.5.gz
%{_mandir}/man5/ovn-*.5.gz
%{_mandir}/man5/vtep.5.gz
%{_mandir}/man7/ovn-architecture.7.gz
%{_mandir}/man7/ovs-fields.7.gz
%{_mandir}/man8/ovs-*.8.gz
%{_mandir}/man8/ovn-*.8.gz
%{_mandir}/man8/vtep-ctl.8.gz

%changelog
*	Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.0-1
-	Update to 2.7.0
*	Fri Feb 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-2
-	Build ovs shared library
*	Wed Nov 16 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-1
-	Update to openvswitch 2.6.1
*	Sat Sep 24 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.5.0-1
-	Update to openvswitch 2.5.0
*	Fri Sep 09 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
-	Update to openvswitch 2.4.1
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.0-3
-	GA - Bump release of all rpms
*       Sat Oct 31 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.0-2
-       OVS requires libatomic.so.1 provided by gcc.
*       Mon Oct 12 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.0-1
-       Update to OVS v2.4.0
*       Fri May 29 2015 Kumar Kaushik <kaushikk@vmware.com> 2.3.1-1
-       Initial build. First version
