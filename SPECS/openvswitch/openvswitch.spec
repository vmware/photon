Summary:        Open vSwitch daemon/database/utilities
Name:           openvswitch
Version:        2.14.0
Release:        14%{?dist}
License:        ASL 2.0 and LGPLv2+
URL:            http://www.openvswitch.org/
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://openvswitch.org/releases/%{name}-%{version}.tar.gz
%define sha512 %{name}=5fe377f9b2857e238e3d40e4452e8b36c80283230f1d0f4b983324532beba725913da817e545c8d7630762f170bb5b0dfe810fd1b8b559994d5eae828beb8ec1

Patch0: openvswitch-CVE-2020-35498.patch
Patch1: openvswitch-CVE-2020-27827.patch
Patch2: openvswitch-CVE-2021-36980.patch
Patch3: openvswitch-CVE-2021-3905.patch
Patch4: openvswitch-CVE-2022-4337-CVE-2022-4338.patch
Patch5: CVE-2023-1668.patch
Patch6: CVE-2023-5366.patch

BuildRequires: gcc
BuildRequires: libcap-ng
BuildRequires: libcap-ng-devel
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: systemd-devel
BuildRequires: python3-devel
BuildRequires: python3-six
BuildRequires: python3-xml

%if 0%{?with_check}
BuildRequires: python3-sortedcontainers
%endif

Requires: libgcc-atomic
Requires: libcap-ng
Requires: openssl
Requires: python3
Requires: python3-six
Requires: python3-xml
Requires: gawk

%description
Open vSwitch provides standard network bridging functions and
support for the OpenFlow protocol for remote per-flow control of
traffic.

%package -n     python3-%{name}
Summary:        python3-%{name}
Requires:       python3
Requires:       %{name} = %{version}

%description -n python3-%{name}
Python 3 version.

%package        devel
Summary:        Header and development files for openvswitch
Requires:       %{name} = %{version}-%{release}

%description    devel
openvswitch-devel package contains header files and libs.

%package        devel-static
Summary:        Static libs for openvswitch
Requires:       %{name} = %{version}-%{release}

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
%configure \
    --enable-ssl \
    --enable-shared

%make_build

%install
%make_install %{?_smp_mflags}
mkdir -p %{buildroot}%{python3_sitelib}

cp -a %{buildroot}%{_datadir}/%{name}/python/ovs \
       %{buildroot}%{python3_sitelib}

mkdir -p %{buildroot}%{_unitdir}
install -p -D -m 0644 \
    rhel/usr_share_%{name}_scripts_systemd_sysconfig.template \
    %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%{python3} build-aux/dpdkstrip.py --nodpdk < \
        rhel/usr_lib_systemd_system_ovs-vswitchd.service.in > \
        rhel/usr_lib_systemd_system_ovs-vswitchd.service

for service in %{name} ovsdb-server ovs-vswitchd; do
  install -p -D -m 0644 rhel/usr_lib_systemd_system_${service}.service \
      %{buildroot}%{_unitdir}/${service}.service
done

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -p -D -m 0644 rhel/etc_%{name}_default.conf \
            %{buildroot}%{_sysconfdir}/%{name}/default.conf

sed -i '/OVS_USER_ID=.*/c\OVS_USER_ID=' %{buildroot}%{_sysconfdir}/%{name}/default.conf

%if 0%{?with_check}
%check
%make_build check
%endif

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
%{_unitdir}/%{name}.service
%{_unitdir}/ovs-vswitchd.service
%{_unitdir}/ovsdb-server.service
%{_libdir}/*.so.*
%{_sysconfdir}/%{name}/default.conf
%{_sysconfdir}/bash_completion.d/ovs-*-bashcomp.bash
%{_datadir}/%{name}/*.ovsschema
%{_datadir}/%{name}/python/*
%{_datadir}/%{name}/scripts/ovs-*
%{_datadir}/%{name}/bugtool-plugins/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}

%files -n python3-%{name}
%defattr(-,root,root)
%{python3_sitelib}/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/openflow/*.h
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/*.pc

%files devel-static
%defattr(-,root,root)
%{_libdir}/*.a

%files doc
%defattr(-,root,root)
%{_mandir}/man1/ovs-*.1.gz
%{_mandir}/man1/ovsdb-*.1.gz
%{_mandir}/man5/ovs-vswitchd.conf.db.5.gz
%{_mandir}/man5/vtep.5.gz
%{_mandir}/man7/ovs-fields.7.gz
%{_mandir}/man8/ovs-*.8.gz
%{_mandir}/man8/vtep-ctl.8.gz
%{_mandir}/man5/ovsdb-server.5.gz
%{_mandir}/man7/ovs-actions.7.gz

%changelog
* Thu Oct 19 2023 Anmol Jain <anmolja@vmware.com> 2.14.0-14
- Fix for CVE-2023-5366
* Thu May 04 2023 Anmol Jain <anmolja@vmware.com> 2.14.0-13
- Fix for CVE-2023-1668
* Tue Jan 17 2023 Dweep Advani <dadvani@vmware.com> 2.14.0-12
- Fixed CVE-2022-4337 and CVE-2022-4338
* Tue Oct 18 2022 Harinadh D <hdommaraju@vmware.com> 2.14.0-11
- fix CVE-2021-3905
* Wed Jan 05 2022 Dweep Advani <dadvani@vmware.com> 2.14.0-10
- Package static libs only in openvswitch-devel-static
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.14.0-9
- Bump up to compile with python 3.10
* Thu Sep 02 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.14.0-8
- Bump up release for openssl
* Wed Sep 01 2021 Sujay G <gsujay@vmware.com> 2.14.0-7
- Fix check_spec.py errors
* Tue Aug 17 2021 Dweep Advani <dadvani@vmware.com> 2.14.0-6
- Patched for CVE-2021-36980
* Thu Apr 01 2021 Dweep Advani <dadvani@vmware.com> 2.14.0-5
- Patched for CVE-2020-27827
* Mon Mar 01 2021 Dweep Advani <dadvani@vmware.com> 2.14.0-4
- Patched for CVE-2020-35498
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.14.0-3
- openssl 1.1.1
* Fri Sep 18 2020 Tapas Kundu <tkundu@vmware.com> 2.14.0-2
- Packged python bindings in right path
* Wed Aug 19 2020 Tapas Kundu <tkundu@vmware.com> 2.14.0-1
- Updated to 2.14
- Removed ovn packages.
* Sun Jul 26 2020 Tapas Kundu <tkundu@vmware.com> 2.12.0-3
- Fix fix_dict_change
* Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 2.12.0-2
- Mass removal python2
* Wed Feb 05 2020 Tapas Kundu <tkundu@vmware.com> 2.12.0-1
- Build with Python3
* Tue Nov 13 2018 Anish Swaminathan <anishs@vmware.com> 2.8.2-3
- Replace with configure macro
* Wed Feb 28 2018 Vinay Kulkarni <kulkarniv@vmware.com> 2.8.2-2
- Setup the default conf file for local ovsdb server.
* Tue Feb 27 2018 Vinay Kulkarni <kulkarniv@vmware.com> 2.8.2-1
- Update to OVS 2.8.2
* Tue Oct 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.7.0-9
- Fix CVE-2017-14970
* Wed Oct 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.7.0-8
- Fix CVE-2017-9263
* Tue Sep 19 2017 Anish Swaminathan <anishs@vmware.com> 2.7.0-7
- Add gawk to Requires
* Tue Aug 29 2017 Sarah Choi <sarahc@vmware.com> 2.7.0-6
- Add python2/python-six/python-xml to Requires
* Thu Jul 13 2017 Nishant Nelogal <nnelogal@vmware.com> 2.7.0-5
- Created OVN packages and systemd service scripts
* Fri Jun 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.0-4
- Fix CVE-2017-9214, CVE-2017-9265
* Mon Jun 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.0-3
- Fix CVE-2017-9264
* Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-2
- Added python and python3 subpackage.
* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.0-1
- Update to 2.7.0
* Fri Feb 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-2
- Build ovs shared library
* Wed Nov 16 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-1
- Update to openvswitch 2.6.1
* Sat Sep 24 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.5.0-1
- Update to openvswitch 2.5.0
* Fri Sep 09 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
- Update to openvswitch 2.4.1
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.0-3
- GA - Bump release of all rpms
* Sat Oct 31 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.0-2
- OVS requires libatomic.so.1 provided by gcc.
* Mon Oct 12 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.0-1
- Update to OVS v2.4.0
* Fri May 29 2015 Kumar Kaushik <kaushikk@vmware.com> 2.3.1-1
- Initial build. First version
