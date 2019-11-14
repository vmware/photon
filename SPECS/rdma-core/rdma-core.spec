%define python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")

Summary:        RDMA Core Userspace Libraries and Daemons
Name:           rdma-core
Version:        26.0
Release:        1%{?dist}
License:        BSD and MIT and GPLv2 and Creative Commons
Group:          Applications/System
URL:            https://github.com/linux-rdma/rdma-core
Source0:        https://github.com/linux-rdma/rdma-core/releases/download/v%{version}/%{name}-%{version}.tar.gz
%define sha1 rdma=5842fbf5833d01a0c3cd0ee8eff7b78436d83024
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  libnl-devel
BuildRequires:  systemd-devel
BuildRequires:  python3-devel
BuildRequires:  python3-xml
BuildRequires:  cython3
Requires:       libnl
Requires:       systemd

%description
Userspace libraries and daemons for the Linux Kernel's drivers/infiniband subsystem.

%package devel
Summary:        Libraries and headers for the rdma-core
Requires:       %{name} = %{version}-%{release}
Requires:       libibverbs = %{version}-%{release}
Requires:       librdmacm = %{version}-%{release}
Requires:       libibumad = %{version}-%{release}
Requires:       libmlx4 = %{version}-%{release}
Requires:       libmlx5 = %{version}-%{release}
Requires:       infiniband-diags = %{version}-%{release}

Provides:       libibverbs-devel = %{version}-%{release}
Provides:       libibumad-devel = %{version}-%{release}
Provides:       librdmacm-devel = %{version}-%{release}
Provides:       ibacm-devel = %{version}-%{release}
Provides:       infiniband-diags-devel = %{version}-%{release}
Provides:       libibmad-devel = %{version}-%{release}
%description devel
Headers and static libraries for the rdma-core

%package -n     libibverbs
Summary:        Library & drivers for direct userspace use of InfiniBand hardware
Requires:       %{name} = %{version}-%{release}
Requires:       libmlx4 = %{version}-%{release}
Requires:       libmlx5 = %{version}-%{release}
%description -n libibverbs
libibverbs is a library that allows userspace processes to use RDMA
"verbs" as described in the InfiniBand Architecture Specification and
the RDMA Protocol Verbs Specification.

%package -n     libibverbs-utils
Summary:        Examples for the libibverbs library
Requires:       libibverbs = %{version}-%{release}
%description -n libibverbs-utils
Useful libibverbs example programs such as ibv_devinfo, which
displays information about RDMA devices.

%package -n     libibmad
Summary:        Libibmad runtime library
Requires:       libibumad
%description -n libibmad
Libibmad provides low layer IB functions for use by the IB diagnostic
and management programs. These include MAD, SA, SMP, and other basic IB
functions. This package contains the runtime library.

%package -n     libibnetdisc
Summary:        Infiniband Net Discovery runtime library
Requires:       libibumad
Requires:       libibmad
%description -n libibnetdisc
This package contains the Infiniband Net Discovery runtime library needed
mainly by infiniband-diags.

%package -n     libmlx4
Summary:        MLX4 runtime library
%description -n libmlx4
This package contains the mlx4 runtime library.

%package -n     libmlx5
Summary:        MLX5 runtime library
%description -n libmlx5
This package contains the mlx5 runtime library.

%package -n     ibacm
Summary:        InfiniBand Communication Manager Assistant
Requires:       %{name} = %{version}-%{release}
%description -n ibacm
The ibacm daemon helps reduce the load of managing path record lookups on
large InfiniBand fabrics by providing a user space implementation of what
is functionally similar to an ARP cache.

%package -n infiniband-diags
Summary:        InfiniBand Diagnostic Tools
Requires:       perl
Requires:       libibnetdisc
Provides:       perl(IBswcountlimits)
%description -n infiniband-diags
It provides IB diagnostic tools.

%package -n     iwpmd
Summary:        Userspace iWarp Port Mapper daemon
Requires:       %{name} = %{version}-%{release}
%description -n iwpmd
iwpmd provides a userspace service for iWarp drivers to claim
tcp ports through the standard socket interface.

%package -n     libibumad
Summary:        OpenFabrics Alliance InfiniBand Userspace Management Datagram library
%description -n libibumad
libibumad provides the userspace management datagram (umad) library
functions, which sit on top of the umad modules in the kernel. These
are used by the IB diagnostic and management tools, including OpenSM.

%package -n     librdmacm
Summary:        Userspace RDMA Connection Manager
Group:          System/Libraries
Requires:       %{name} = %{version}-%{release}
%description -n librdmacm
librdmacm provides a userspace RDMA Communication Management API.

%package -n     librdmacm-utils
Summary:        Examples for the librdmacm library
%description -n librdmacm-utils
Example test programs for the librdmacm library.

%package -n     srp_daemon
Summary:        Tools for using the InfiniBand SRP protocol devices
Requires:       %{name} = %{version}-%{release}
Provides:       srptools = %{version}-%{release}
%description -n srp_daemon
In conjunction with the kernel ib_srp driver, srp_daemon allows you to
discover and use SCSI devices via the SCSI RDMA Protocol over InfiniBand.

%package -n     rdma-ndd
Summary:        Daemon to manage RDMA Node Description
Requires:       %{name} = %{version}-%{release}
%description -n rdma-ndd
rdma-ndd is a system daemon which watches for rdma device changes and/or
hostname changes and updates the Node Description of the rdma devices based
on those changes.

%package -n python3-pyverbs
Summary:        Python3 API over IB verbs
%description -n python3-pyverbs
Pyverbs is a Cython-based Python API over libibverbs, providing an
easy, object-oriented access to IB verbs.

%prep
%setup -q
%build
cmake \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_BINDIR:PATH=%{_bindir} \
        -DCMAKE_INSTALL_SBINDIR:PATH=%{_sbindir} \
        -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
        -DCMAKE_INSTALL_LIBEXECDIR:PATH=%{_libexecdir} \
        -DCMAKE_INSTALL_LOCALSTATEDIR:PATH=%{_localstatedir} \
        -DCMAKE_INSTALL_SHAREDSTATEDIR:PATH=%{_sharedstatedir} \
        -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir} \
        -DCMAKE_INSTALL_INFODIR:PATH=%{_infodir} \
        -DCMAKE_INSTALL_MANDIR:PATH=%{_mandir} \
        -DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_sysconfdir} \
        -DCMAKE_INSTALL_SYSTEMD_SERVICEDIR:PATH=%{_unitdir} \
        -DCMAKE_INSTALL_SYSTEMD_BINDIR:PATH=%{_libexecdir}/systemd \
        -DCMAKE_INSTALL_INITDDIR:PATH=%{_initddir} \
        -DCMAKE_INSTALL_RUNDIR:PATH=%{_rundir} \
        -DCMAKE_INSTALL_DOCDIR:PATH=%{_docdir}/%{name}-%{version} \
        -DCMAKE_INSTALL_UDEV_RULESDIR:PATH=%{_udevrulesdir} \
        -DCMAKE_INSTALL_PERLDIR:PATH=%{perl_vendorlib} \
        -DCMAKE_INSTALL_PYTHON_ARCH_LIB:PATH=%{python3_sitearch} \
        -GNinja
%ninja_build

%install
# pandoc is not available - create missing prebuilt pandoc files.
cat infiniband-diags/man/cmake_install.cmake | grep prebuilt | sed 's/^.*prebuilt\///;s/")//' | xargs -n1 -i touch buildlib/pandoc-prebuilt/{}

%ninja_install

# Remove init.d scripts
rm -rf %{buildroot}/%{_sysconfdir}/rc.d
rm -rf %{buildroot}/%{_sbindir}/srp_daemon.sh

%check
cd build && make %{?_smp_mflags} check

%post -n libibverbs -p /sbin/ldconfig
%postun -n libibverbs -p /sbin/ldconfig

%post -n libmlx4 -p /sbin/ldconfig
%postun -n libmlx4 -p /sbin/ldconfig

%post -n libmlx5 -p /sbin/ldconfig
%postun -n libmlx5 -p /sbin/ldconfig

%post -n libibumad -p /sbin/ldconfig
%postun -n libibumad -p /sbin/ldconfig

%post -n librdmacm -p /sbin/ldconfig
%postun -n librdmacm -p /sbin/ldconfig

%post -n libibnetdisc -p /sbin/ldconfig
%postun -n libibnetdisc -p /sbin/ldconfig

%post -n libibmad -p /sbin/ldconfig
%postun -n libibmad -p /sbin/ldconfig

%post
# trigger udev update.
/usr/bin/udevadm trigger --subsystem-match=infiniband --action=change || true
/usr/bin/udevadm trigger --subsystem-match=infiniband_mad --action=change || true

#
# ibacm
#
%post -n ibacm
%systemd_post ibacm.service
%preun -n ibacm
%systemd_preun ibacm.service
%postun -n ibacm
%systemd_postun_with_restart ibacm.service

#
# srp daemon
#
%post -n srp_daemon
%systemd_post srp_daemon.service
# trigger udev update.
/usr/bin/udevadm trigger --subsystem-match=infiniband_mad --action=change
%preun -n srp_daemon
%systemd_preun srp_daemon.service
%postun -n srp_daemon
%systemd_postun_with_restart srp_daemon.service

#
# iwpmd
#
%post -n iwpmd
%systemd_post iwpmd.service
%preun -n iwpmd
%systemd_preun iwpmd.service
%postun -n iwpmd
%systemd_postun_with_restart iwpmd.service

#
# rdma-ndd
#
%post -n rdma-ndd
%systemd_post rdma-ndd.service
%preun -n rdma-ndd
%systemd_preun rdma-ndd.service
%postun -n rdma-ndd
%systemd_postun_with_restart rdma-ndd.service

%files
%defattr(-,root,root)
%{_sysconfdir}/modprobe.d/*
%dir %{_sysconfdir}/rdma/modules
%config(noreplace) %{_sysconfdir}/rdma/modules/infiniband.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/iwarp.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/opa.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/rdma.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/roce.conf
%config(noreplace) %{_sysconfdir}/udev/rules.d/70-persistent-ipoib.rules
%{_unitdir}/rdma-hw.target
%{_unitdir}/rdma-load-modules@.service
/lib/udev/rdma_rename
%{_udevrulesdir}/60-rdma-persistent-naming.rules
%{_udevrulesdir}/75-rdma-description.rules
%{_udevrulesdir}/90-rdma-hw-modules.rules
%{_udevrulesdir}/90-rdma-ulp-modules.rules
%{_udevrulesdir}/90-rdma-umad.rules
%{_libexecdir}/truescale-serdes.cmds
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/README.md
%doc %{_docdir}/%{name}-%{version}/udev.md
%license COPYING.*

%files devel
%defattr(-,root,root)
%{_mandir}/man7/efadv*
%{_mandir}/man7/mlx4dv*
%{_mandir}/man7/mlx5dv*
%{_mandir}/man7/rdma_cm.*
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libefa.so
%{_libdir}/libibmad.so
%{_libdir}/libibnetdisc.so
%{_libdir}/libibumad.so
%{_libdir}/libibverbs.so
%{_libdir}/libmlx4.so
%{_libdir}/libmlx5.so
%{_libdir}/librdmacm.so
%{_mandir}/man3/*
%doc %{_docdir}/%{name}-%{version}/MAINTAINERS

%files -n libibverbs
%defattr(-,root,root)
%dir %{_sysconfdir}/libibverbs.d
%config(noreplace) %{_sysconfdir}/libibverbs.d/*.driver
%{_bindir}/rxe_cfg
%{_libdir}/libefa.so.*
%{_libdir}/libibverbs*.so.*
%dir %{_libdir}/libibverbs
%{_libdir}/libibverbs/*.so
%{_mandir}/man7/rxe*
%{_mandir}/man8/rxe*
%doc %{_docdir}/%{name}-%{version}/libibverbs.md
%doc %{_docdir}/%{name}-%{version}/rxe.md
%doc %{_docdir}/%{name}-%{version}/tag_matching.md

%files -n libibverbs-utils
%defattr(-,root,root)
%{_bindir}/ibv_*
%{_mandir}/man1/ibv_*

%files -n libibmad
%defattr(-, root, root)
%{_libdir}/libibmad.so.*

%files -n libibnetdisc
%defattr(-, root, root)
%{_libdir}/libibnetdisc.so.*

%files -n libmlx4
%defattr(-,root,root)
%{_libdir}/libmlx4*.so.*

%files -n libmlx5
%defattr(-,root,root)
%{_libdir}/libmlx5*.so.*

%files -n ibacm
%defattr(-,root,root)
%{_unitdir}/ibacm.service
%{_unitdir}/ibacm.socket
%{_bindir}/ib_acme
%dir %{_libdir}/ibacm
%{_libdir}/ibacm/*
%{_sbindir}/ibacm
%{_mandir}/man1/ib_acme.*
%{_mandir}/man1/ibacm.*
%{_mandir}/man7/ibacm.*
%{_mandir}/man7/ibacm_prov.*
%doc %{_docdir}/%{name}-%{version}/ibacm.md

%files -n infiniband-diags
%defattr(-, root, root)
%dir %{_sysconfdir}/infiniband-diags
%config(noreplace) %{_sysconfdir}/infiniband-diags/*
%{perl_vendorlib}/IBswcountlimits.pm
%{_sbindir}/check_lft_balance.pl
%{_sbindir}/dump_fts
%{_sbindir}/dump_lfts.sh
%{_sbindir}/dump_mfts.sh
%{_sbindir}/ibaddr
%{_sbindir}/ibcacheedit
%{_sbindir}/ibccconfig
%{_sbindir}/ibccquery
%{_sbindir}/ibfindnodesusing.pl
%{_sbindir}/ibhosts
%{_sbindir}/ibidsverify.pl
%{_sbindir}/iblinkinfo
%{_sbindir}/ibnetdiscover
%{_sbindir}/ibnodes
%{_sbindir}/ibping
%{_sbindir}/ibportstate
%{_sbindir}/ibqueryerrors
%{_sbindir}/ibroute
%{_sbindir}/ibrouters
%{_sbindir}/ibstat
%{_sbindir}/ibstatus
%{_sbindir}/ibswitches
%{_sbindir}/ibsysstat
%{_sbindir}/ibtracert
%{_sbindir}/perfquery
%{_sbindir}/saquery
%{_sbindir}/sminfo
%{_sbindir}/smpdump
%{_sbindir}/smpquery
%{_sbindir}/vendstat
%{_mandir}/man8/check_lft_balance*
%{_mandir}/man8/dump_fts*
%{_mandir}/man8/dump_lfts*
%{_mandir}/man8/dump_mfts*
%{_mandir}/man8/ibaddr*
%{_mandir}/man8/ibcacheedit*
%{_mandir}/man8/ibccconfig*
%{_mandir}/man8/ibccquery*
%{_mandir}/man8/ibfindnodesusing*
%{_mandir}/man8/ibhosts*
%{_mandir}/man8/ibidsverify*
%{_mandir}/man8/iblinkinfo*
%{_mandir}/man8/ibnetdiscover*
%{_mandir}/man8/ibnodes*
%{_mandir}/man8/ibping*
%{_mandir}/man8/ibportstate*
%{_mandir}/man8/ibqueryerrors*
%{_mandir}/man8/ibroute.*
%{_mandir}/man8/ibrouters*
%{_mandir}/man8/ibstat.*
%{_mandir}/man8/ibstatus*
%{_mandir}/man8/ibswitches*
%{_mandir}/man8/ibsysstat*
%{_mandir}/man8/ibtracert*
%{_mandir}/man8/infiniband-diags*
%{_mandir}/man8/perfquery*
%{_mandir}/man8/saquery*
%{_mandir}/man8/sminfo*
%{_mandir}/man8/smpdump*
%{_mandir}/man8/smpquery*
%{_mandir}/man8/vendstat*

%files -n iwpmd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/iwpmd.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/iwpmd.conf
%{_unitdir}/iwpmd.service
%{_udevrulesdir}/90-iwpmd.rules
%{_sbindir}/iwpmd
%{_mandir}/man5/iwpmd.*
%{_mandir}/man8/iwpmd.*

%files -n libibumad
%defattr(-,root,root)
%{_libdir}/libibumad*.so.*

%files -n librdmacm
%defattr(-,root,root)
%{_libdir}/librdmacm*.so.*
%dir %{_libdir}/rsocket
%{_libdir}/rsocket/*.so*
%{_mandir}/man7/rsocket.*
%doc %{_docdir}/%{name}-%{version}/librdmacm.md

%files -n librdmacm-utils
%defattr(-,root,root)
%{_bindir}/cmtime
%{_bindir}/mckey
%{_bindir}/rcopy
%{_bindir}/rdma_client
%{_bindir}/rdma_server
%{_bindir}/rdma_xclient
%{_bindir}/rdma_xserver
%{_bindir}/riostream
%{_bindir}/rping
%{_bindir}/rstream
%{_bindir}/ucmatose
%{_bindir}/udaddy
%{_bindir}/udpong
%{_mandir}/man1/cmtime.*
%{_mandir}/man1/mckey.*
%{_mandir}/man1/rcopy.*
%{_mandir}/man1/rdma_client.*
%{_mandir}/man1/rdma_server.*
%{_mandir}/man1/rdma_xclient.*
%{_mandir}/man1/rdma_xserver.*
%{_mandir}/man1/riostream.*
%{_mandir}/man1/rping.*
%{_mandir}/man1/rstream.*
%{_mandir}/man1/ucmatose.*
%{_mandir}/man1/udaddy.*
%{_mandir}/man1/udpong.*

%files -n srp_daemon
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/rdma/modules/srp_daemon.conf
%config(noreplace) %{_sysconfdir}/srp_daemon.conf
%{_unitdir}/srp_daemon.service
%{_unitdir}/srp_daemon_port@.service
%{_udevrulesdir}/60-srp_daemon.rules
%dir %{_libexecdir}/srp_daemon
%{_libexecdir}/srp_daemon/start_on_all_ports
%{_sbindir}/ibsrpdm
%{_sbindir}/run_srp_daemon
%{_sbindir}/srp_daemon
%{_mandir}/man1/ibsrpdm.1*
%{_mandir}/man1/srp_daemon.1*
%{_mandir}/man5/srp_daemon.service.5*
%{_mandir}/man5/srp_daemon_port@.service.5*
%doc %{_docdir}/%{name}-%{version}/ibsrpdm.md

%files -n rdma-ndd
%defattr(-, root, root)
%{_unitdir}/rdma-ndd.service
%{_udevrulesdir}/60-rdma-ndd.rules
%{_sbindir}/rdma-ndd
%{_mandir}/man8/rdma-ndd.8*

%files -n python3-pyverbs
%defattr(-,root,root)
%{python3_sitearch}/pyverbs

%changelog
* Fri Nov 08 2019 Alexey Makhalov <amakhalov@vmware.com> 26.0-1
- Initial build.
