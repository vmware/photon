Summary:        Open vSwitch daemon/database/utilities
Name:           openvswitch
Version:        2.3.1
Release:        1%{?dist}
License:        ASL 2.0 and LGPLv2+
URL:            http://www.openvswitch.org/
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://openvswitch.org/releases/%{name}-%{version}.tar.gz
%define sha1 openvswitch=ef8854781265a7e3ea80b5070db6cac2dff704d5
Requires: openssl
BuildRequires: openssl openssl-devel python2 python2-devel
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs
Requires:       python-configobj
Requires:       python-prettytable
Requires:       python-requests
Requires:       PyYAML
Requires:       python-jsonpatch

%description
Open vSwitch provides standard network bridging functions and
support for the OpenFlow protocol for remote per-flow control of
traffic.

%prep
%setup -q

%build
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=/etc \
            --localstatedir=/var \
            --enable-ssl

make %{_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root)
%{_bindir}/*
/usr/lib/libofproto.a
/usr/lib/libofproto.la
/usr/lib/libopenvswitch.a
/usr/lib/libopenvswitch.la
/usr/lib/libovsdb.a
/usr/lib/libovsdb.la
/usr/lib/libsflow.a
/usr/lib/libsflow.la
/usr/sbin/ovs-bugtool
/usr/sbin/ovs-vlan-bug-workaround
/usr/sbin/ovs-vswitchd
/usr/sbin/ovsdb-server
/usr/share/man/man1/ovs-benchmark.1.gz
/usr/share/man/man1/ovs-pcap.1.gz
/usr/share/man/man1/ovs-tcpundump.1.gz
/usr/share/man/man1/ovsdb-client.1.gz
/usr/share/man/man1/ovsdb-server.1.gz
/usr/share/man/man1/ovsdb-tool.1.gz
/usr/share/man/man5/ovs-vswitchd.conf.db.5.gz
/usr/share/man/man5/vtep.5.gz
/usr/share/man/man8/ovs-appctl.8.gz
/usr/share/man/man8/ovs-bugtool.8.gz
/usr/share/man/man8/ovs-ctl.8.gz
/usr/share/man/man8/ovs-dpctl-top.8.gz
/usr/share/man/man8/ovs-dpctl.8.gz
/usr/share/man/man8/ovs-l3ping.8.gz
/usr/share/man/man8/ovs-ofctl.8.gz
/usr/share/man/man8/ovs-parse-backtrace.8.gz
/usr/share/man/man8/ovs-pki.8.gz
/usr/share/man/man8/ovs-test.8.gz
/usr/share/man/man8/ovs-vlan-bug-workaround.8.gz
/usr/share/man/man8/ovs-vlan-test.8.gz
/usr/share/man/man8/ovs-vsctl.8.gz
/usr/share/man/man8/ovs-vswitchd.8.gz
/usr/share/man/man8/vtep-ctl.8.gz
/usr/share/openvswitch/bugtool-plugins/kernel-info/openvswitch.xml
/usr/share/openvswitch/bugtool-plugins/network-status/openvswitch.xml
/usr/share/openvswitch/bugtool-plugins/system-configuration.xml
/usr/share/openvswitch/bugtool-plugins/system-configuration/openvswitch.xml
/usr/share/openvswitch/bugtool-plugins/system-logs/openvswitch.xml
/usr/share/openvswitch/python/ovs/__init__.py
/usr/share/openvswitch/python/ovs/daemon.py
/usr/share/openvswitch/python/ovs/db/__init__.py
/usr/share/openvswitch/python/ovs/db/data.py
/usr/share/openvswitch/python/ovs/db/error.py
/usr/share/openvswitch/python/ovs/db/idl.py
/usr/share/openvswitch/python/ovs/db/parser.py
/usr/share/openvswitch/python/ovs/db/schema.py
/usr/share/openvswitch/python/ovs/db/types.py
/usr/share/openvswitch/python/ovs/dirs.py
/usr/share/openvswitch/python/ovs/fatal_signal.py
/usr/share/openvswitch/python/ovs/json.py
/usr/share/openvswitch/python/ovs/jsonrpc.py
/usr/share/openvswitch/python/ovs/ovsuuid.py
/usr/share/openvswitch/python/ovs/poller.py
/usr/share/openvswitch/python/ovs/process.py
/usr/share/openvswitch/python/ovs/reconnect.py
/usr/share/openvswitch/python/ovs/socket_util.py
/usr/share/openvswitch/python/ovs/stream.py
/usr/share/openvswitch/python/ovs/timeval.py
/usr/share/openvswitch/python/ovs/unixctl/__init__.py
/usr/share/openvswitch/python/ovs/unixctl/client.py
/usr/share/openvswitch/python/ovs/unixctl/server.py
/usr/share/openvswitch/python/ovs/util.py
/usr/share/openvswitch/python/ovs/version.py
/usr/share/openvswitch/python/ovs/vlog.py
/usr/share/openvswitch/python/ovstest/__init__.py
/usr/share/openvswitch/python/ovstest/args.py
/usr/share/openvswitch/python/ovstest/rpcserver.py
/usr/share/openvswitch/python/ovstest/tcp.py
/usr/share/openvswitch/python/ovstest/tests.py
/usr/share/openvswitch/python/ovstest/udp.py
/usr/share/openvswitch/python/ovstest/util.py
/usr/share/openvswitch/python/ovstest/vswitch.py
/usr/share/openvswitch/scripts/ovs-bugtool-bfd-show
/usr/share/openvswitch/scripts/ovs-bugtool-bond-show
/usr/share/openvswitch/scripts/ovs-bugtool-cfm-show
/usr/share/openvswitch/scripts/ovs-bugtool-coverage-show
/usr/share/openvswitch/scripts/ovs-bugtool-daemons-ver
/usr/share/openvswitch/scripts/ovs-bugtool-lacp-show
/usr/share/openvswitch/scripts/ovs-bugtool-list-dbs
/usr/share/openvswitch/scripts/ovs-bugtool-memory-show
/usr/share/openvswitch/scripts/ovs-bugtool-ovs-appctl-dpif
/usr/share/openvswitch/scripts/ovs-bugtool-ovs-ofctl-dump-flows
/usr/share/openvswitch/scripts/ovs-bugtool-ovs-ofctl-show
/usr/share/openvswitch/scripts/ovs-bugtool-ovsdb-dump
/usr/share/openvswitch/scripts/ovs-bugtool-tc-class-show
/usr/share/openvswitch/scripts/ovs-bugtool-vsctl-show
/usr/share/openvswitch/scripts/ovs-check-dead-ifs
/usr/share/openvswitch/scripts/ovs-ctl
/usr/share/openvswitch/scripts/ovs-lib
/usr/share/openvswitch/scripts/ovs-save
/usr/share/openvswitch/scripts/ovs-vtep
/usr/share/openvswitch/vswitch.ovsschema
/usr/share/openvswitch/vtep.ovsschema

%changelog
*       Fri May 29 2015 Kumar Kaushik <kaushikk@vmware.com> 2.3.1-1
-       Initial build. First version

