Summary:        Open vSwitch daemon/database/utilities
Name:           openvswitch
Version:        2.6.1
Release:        2%{?dist}
License:        ASL 2.0 and LGPLv2+
URL:            http://www.openvswitch.org/
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://openvswitch.org/releases/%{name}-%{version}.tar.gz
%define sha1 openvswitch=2865fe03b3906b5aea984102c4b65772b5dd7450

%global kernelver 4.4.60-1.ph1

BuildRequires:  gcc >= 4.0.0
BuildRequires:  kmod
BuildRequires:  libcap-ng
BuildRequires:  libcap-ng-devel
BuildRequires:  linux
BuildRequires:  linux-dev
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

%package -n     kmod-%{name}
Summary:        Open vSwitch kernel modules
Group:          Development/Libraries

%description -n kmod-%{name}
This package provides openvswitch kernel modules.

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
        --with-linux=/usr/lib/modules/%{kernelver}/build 'CFLAGS=-O2 -g'
make %{_smp_mflags}

%install
make DESTDIR=%{buildroot} install
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/openvswitch
make modules_install

find %{buildroot}%{_libdir} -name '*.la' -delete
find $INSTALL_MOD_PATH/lib/modules -iname 'modules.*' -exec rm {} \;

install -d %{buildroot}%{_sysconfdir}/depmod.d/
for module in %{buildroot}/lib/modules/%{kernel_version}/$INSTALL_MOD_DIR/*.ko;
do
    modname="$(basename ${module})"
    echo "override ${modname%.ko} * extra/openvswitch" >> openvswitch.conf
    echo "override ${modname%.ko} * weak-updates/openvswitch" >> openvswitch.conf
done
install -m 644 openvswitch.conf %{buildroot}%{_sysconfdir}/depmod.d/

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
/etc/bash_completion.d/ovs-*-bashcomp.bash
/usr/share/openvswitch/*.ovsschema
/usr/share/openvswitch/bugtool-plugins/*
/usr/share/openvswitch/python/*
/usr/share/openvswitch/scripts/ovs-*
/usr/share/openvswitch/scripts/ovn-*

%files devel
%{_includedir}/ovn/*.h
%{_includedir}/openflow/*.h
%{_includedir}/openvswitch/*.h
%{_libdir}/lib*
%{_libdir}/pkgconfig/*.pc

%files doc
/usr/share/man/man1/ovs-*.1.gz
/usr/share/man/man1/ovsdb-*.1.gz
/usr/share/man/man5/ovs-vswitchd.conf.db.5.gz
/usr/share/man/man5/ovn-*.5.gz
/usr/share/man/man5/vtep.5.gz
/usr/share/man/man7/ovn-architecture.7.gz
/usr/share/man/man8/ovs-*.8.gz
/usr/share/man/man8/ovn-*.8.gz
/usr/share/man/man8/vtep-ctl.8.gz

%files -n kmod-%{name}
/etc/depmod.d/openvswitch.conf
/lib/modules/%{kernelver}/extra/openvswitch/openvswitch.ko
/lib/modules/%{kernelver}/extra/openvswitch/vport-geneve.ko
/lib/modules/%{kernelver}/extra/openvswitch/vport-gre.ko
/lib/modules/%{kernelver}/extra/openvswitch/vport-lisp.ko
/lib/modules/%{kernelver}/extra/openvswitch/vport-stt.ko
/lib/modules/%{kernelver}/extra/openvswitch/vport-vxlan.ko

%changelog
*	Fri Feb 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-2
-	Build ovs shared library
*	Wed Nov 16 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-1
-	Update to openvswitch 2.6.1
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.0-3
-	GA - Bump release of all rpms
*       Sat Oct 31 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.0-2
-       OVS requires libatomic.so.1 provided by gcc.
*       Mon Oct 12 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.0-1
-       Update to OVS v2.4.0
*       Fri May 29 2015 Kumar Kaushik <kaushikk@vmware.com> 2.3.1-1
-       Initial build. First version
