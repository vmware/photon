%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Open vSwitch daemon/database/utilities
Name:           openvswitch
Version:        2.17.1
Release:        1%{?dist}
License:        ASL 2.0 and LGPLv2+
URL:            http://www.openvswitch.org/
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://openvswitch.org/releases/%{name}-%{version}.tar.gz
%define sha512  openvswitch=55c7c4d01606aa30ab065e6d181441d0ec8608ccb7ab554fcf4c39494908a0cba0bf961a72b898ab938264e7f1015c2a6d01af20de958fbc698b34543c8ddf10
BuildRequires:  gcc >= 4.0.0
BuildRequires:  libcap-ng
BuildRequires:  libcap-ng-devel
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  systemd
BuildRequires:  python3 >= 3.4.0
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-six
BuildRequires:  python3-xml
Requires:       libgcc-atomic
Requires:       libcap-ng
Requires:       openssl
Requires:       python3
Requires:       python3-libs
Requires:       python3-six
Requires:       python3-xml
Requires:       gawk

%description
Open vSwitch provides standard network bridging functions and
support for the OpenFlow protocol for remote per-flow control of traffic.

%package -n     python3-openvswitch
Summary:        python3-openvswitch
Requires:       python3
Requires:       python3-libs

%description -n python3-openvswitch
Python 3 version.

%package        devel
Summary:        Header and development files for openvswitch
Requires:       %{name} = %{version}

%description    devel
openvswitch-devel package contains header files and libs.

%package        devel-static
Summary:        Static libs for openvswitch
Requires:       %{name} = %{version}

%description    devel-static
openvswitch-devel-static package contains static libs.

%package        doc
Summary:        Documentation for openvswitch
Requires:       %{name} = %{version}-%{release}

%description    doc
It contains the documentation and manpages for openvswitch.

%prep
%autosetup -p1

%build
export PYTHON2=no

%configure --enable-ssl --enable-shared
make %{_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{_smp_mflags}
find %{buildroot}/%{_libdir} -name '*.la' -delete
mkdir -p %{buildroot}/%{python3_sitelib}
cp -a %{buildroot}/%{_datadir}/openvswitch/python/ovs %{buildroot}/%{python3_sitelib}

mkdir -p %{buildroot}/%{_libdir}/systemd/system
install -p -D -m 0644 rhel/usr_share_openvswitch_scripts_systemd_sysconfig.template %{buildroot}/%{_sysconfdir}/sysconfig/openvswitch

/usr/bin/python3 build-aux/dpdkstrip.py --nodpdk < rhel/usr_lib_systemd_system_ovs-vswitchd.service.in > rhel/usr_lib_systemd_system_ovs-vswitchd.service
for service in openvswitch ovsdb-server ovs-vswitchd; do
	install -p -D -m 0644 rhel/usr_lib_systemd_system_${service}.service %{buildroot}/%{_unitdir}/${service}.service
done

mkdir -p %{buildroot}/%{_sysconfdir}/openvswitch
install -p -D -m 0644 rhel/etc_openvswitch_default.conf %{buildroot}/%{_sysconfdir}/openvswitch/default.conf
sed -i '/OVS_USER_ID=.*/c\OVS_USER_ID=' %{buildroot}/%{_sysconfdir}/openvswitch/default.conf

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck} %{_smp_mflags}

%preun
%systemd_preun %{name}.service

%post
%systemd_post %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root)
%{_bindir}/ovs-*
%{_bindir}/ovsdb-*
%{_bindir}/vtep-ctl
%{_sbindir}/ovs-*
%{_sbindir}/ovsdb-server
%{_unitdir}/openvswitch.service
%{_unitdir}/ovs-vswitchd.service
%{_unitdir}/ovsdb-server.service
%{_libdir}/lib*
%{_sysconfdir}/openvswitch/default.conf
%{_sysconfdir}/bash_completion.d/ovs-*-bashcomp.bash
%{_datadir}/openvswitch/*.ovsschema
%{_datadir}/openvswitch/python/*
%{_datadir}/openvswitch/scripts/ovs-*
%{_datadir}/openvswitch/bugtool-plugins/*
%config(noreplace) %{_sysconfdir}/sysconfig/openvswitch

%files -n python3-openvswitch
%{python3_sitelib}/*

%files devel
%{_includedir}/openflow/*.h
%{_includedir}/openvswitch/*.h
%{_libdir}/pkgconfig/*.pc

%files devel-static
%{_libdir}/*.a

%files doc
%{_mandir}/man1/ovs-*.1.gz
%{_mandir}/man1/ovsdb-*.1.gz
%{_mandir}/man5/ovs-vswitchd.conf.db.5.gz
%{_mandir}/man5/vtep.5.gz
%{_mandir}/man7/ovs-fields.7.gz
%{_mandir}/man8/ovs-*.8.gz
%{_mandir}/man8/vtep-ctl.8.gz
%{_mandir}/man5/ovsdb-server.5.gz

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.17.1-1
-   Automatic Version Bump
*   Thu Sep 02 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.15.0-2
-   Bump up release for openssl
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.15.0-1
-   Automatic Version Bump
*   Mon Mar 01 2021 Dweep Advani <dadvani@vmware.com> 2.14.0-4
-   Patched for CVE-2020-35498
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.14.0-3
-   openssl 1.1.1
*   Fri Sep 18 2020 Tapas Kundu <tkundu@vmware.com> 2.14.0-2
-   Packged python bindings in right path
*   Wed Aug 19 2020 Tapas Kundu <tkundu@vmware.com> 2.14.0-1
-   Updated to 2.14
-   Removed ovn packages.
*   Sun Jul 26 2020 Tapas Kundu <tkundu@vmware.com> 2.12.0-3
-   Fix fix_dict_change
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 2.12.0-2
-   Mass removal python2
*   Wed Feb 05 2020 Tapas Kundu <tkundu@vmware.com> 2.12.0-1
-   Build with Python3
*   Tue Nov 13 2018 Anish Swaminathan <anishs@vmware.com> 2.8.2-3
-   Replace with configure macro
*   Wed Feb 28 2018 Vinay Kulkarni <kulkarniv@vmware.com> 2.8.2-2
-   Setup the default conf file for local ovsdb server.
*   Tue Feb 27 2018 Vinay Kulkarni <kulkarniv@vmware.com> 2.8.2-1
-   Update to OVS 2.8.2
*   Tue Oct 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.7.0-9
-   Fix CVE-2.17.14970
*   Wed Oct 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.7.0-8
-   Fix CVE-2017-9263
*   Tue Sep 19 2017 Anish Swaminathan <anishs@vmware.com> 2.7.0-7
-   Add gawk to Requires
*   Tue Aug 29 2017 Sarah Choi <sarahc@vmware.com> 2.7.0-6
-   Add python2/python-six/python-xml to Requires
*   Thu Jul 13 2017 Nishant Nelogal <nnelogal@vmware.com> 2.7.0-5
-   Created OVN packages and systemd service scripts
*   Fri Jun 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.0-4
-   Fix CVE-2017-9214, CVE-2017-9265
*   Mon Jun 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.0-3
-   Fix CVE-2017-9264
*   Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-2
-   Added python and python3 subpackage.
*   Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.0-1
-   Update to 2.7.0
*   Fri Feb 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-2
-   Build ovs shared library
*   Wed Nov 16 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-1
-   Update to openvswitch 2.6.1
*   Sat Sep 24 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.5.0-1
-   Update to openvswitch 2.5.0
*   Fri Sep 09 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
-   Update to openvswitch 2.4.1
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.0-3
-   GA - Bump release of all rpms
*   Sat Oct 31 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.0-2
-   OVS requires libatomic.so.1 provided by gcc.
*   Mon Oct 12 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.0-1
-   Update to OVS v2.4.0
*   Fri May 29 2015 Kumar Kaushik <kaushikk@vmware.com> 2.3.1-1
-   Initial build. First version
