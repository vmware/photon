%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Userland logical volume management tools 
Name:           lvm2
Version:        2.02.181
Release:        1%{?dist}
License:        GPLv2, BSD 2-Clause and LGPLv2.1
Group:          System Environment/Base
URL:            http://sources.redhat.com/dm
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        ftp://sources.redhat.com/pub/lvm2/releases/LVM2.%{version}.tgz
%define sha1    LVM2=2802799c60ef4f61534df1e40bcc29e4e043b29b
Source1:        lvm2-activate.service
Patch0:         lvm2-set-default-preferred_names.patch
BuildRequires:  libselinux-devel, libsepol-devel
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
BuildRequires:  systemd-devel
BuildRequires:  thin-provisioning-tools
BuildRequires:  libaio-devel
Requires:       device-mapper-libs = %{version}-%{release}
Requires:       device-mapper-event-libs = %{version}-%{release}
Requires:       device-mapper-event = %{version}-%{release}
Requires:       device-mapper = %{version}-%{release}
Requires:       systemd

%description
LVM2 includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadd(8) or even loop devices, see
losetup(8)), creating volume groups (kind of virtual disks) from one
or more physical volumes and creating one or more logical volumes
(kind of logical partitions) in volume groups.

%package    devel
Summary:    Development libraries and headers
Group:      Development/Libraries
License:    LGPLv2
Requires:   %{name} = %{version}-%{release}
Requires:   device-mapper-devel = %{version}-%{release}
Requires:   util-linux-devel

%description    devel
This package contains files needed to develop applications that use
the lvm2 libraries.

%package    libs
Summary:    Shared libraries for lvm2
License:    LGPLv2
Group:      System Environment/Libraries
Requires:   device-mapper-libs = %{version}-%{release}
Requires:   device-mapper-event-libs = %{version}-%{release}

%description    libs
This package contains shared lvm2 libraries for applications.

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%package        python-libs
Summary:        Python module to access LVM
License:        LGPLv2
Group:          Development/Libraries
BuildRequires:  python2-devel
Requires:       %{name}-libs = %{version}-%{release}
Requires:       python2-libs
Requires:       python2

%description    python-libs
Python module to allow the creation and use of LVM
logical volumes, physical volumes, and volume groups.

%package    -n  python3-lvm2-libs
Summary:        Python module to access LVM
License:        LGPLv2
Group:          Development/Libraries
BuildRequires:  python3-devel
Requires:       %{name}-libs = %{version}-%{release}
Requires:       python3-libs
Requires:       python3

%description -n python3-lvm2-libs
Python module to allow the creation and use of LVM
logical volumes, physical volumes, and volume groups.

%package -n device-mapper
Summary:    Device mapper utility
Group:      System Environment/Base
URL:        http://sources.redhat.com/dm
Requires:   device-mapper-libs
Requires:   systemd
%description -n device-mapper
This package contains the supporting userspace utility, dmsetup,
for the kernel device-mapper.

%package -n device-mapper-devel
Summary:    Development libraries and headers for device-mapper
License:    LGPLv2
Group:      Development/Libraries
Requires:   device-mapper = %{version}-%{release}
Requires:   libselinux-devel
Provides:   pkgconfig(devmapper)

%description -n device-mapper-devel
This package contains files needed to develop applications that use
the device-mapper libraries.

%package -n device-mapper-libs
Summary:    Device-mapper shared library
License:    LGPLv2
Group:      System Environment/Libraries
Requires:   libselinux
Requires:   libsepol
Requires:   systemd

%description -n device-mapper-libs
This package contains the device-mapper shared library, libdevmapper.

%post -n device-mapper-libs 
/sbin/ldconfig

%postun -n device-mapper-libs
/sbin/ldconfig

%package -n device-mapper-event
Summary:    Device-mapper event daemon
Group:      System Environment/Base
Requires:   device-mapper = %{version}-%{release}
Requires:   device-mapper-event-libs = %{version}-%{release}
Requires:       systemd

%description -n device-mapper-event
This package contains the dmeventd daemon for monitoring the state
of device-mapper devices.

%post -n device-mapper-event
%systemd_post dm-event.service dm-event.socket 
if [ $1 -eq 1 ];then
    # This is initial installation
    systemctl start dm-event.socket
fi
%preun -n device-mapper-event
if [ $1 -eq 0 ];then
    # This is erase operation
    systemctl stop dm-event.socket
fi
%systemd_preun dm-event.service dm-event.socket

%postun -n device-mapper-event
%systemd_postun_with_restart dm-event.service dm-event.socket

%package -n device-mapper-event-libs
Summary:    Device-mapper event daemon shared library
License:    LGPLv2
Group:      System Environment/Libraries
Requires:   device-mapper-libs = %{version}-%{release}

%description -n device-mapper-event-libs
This package contains the device-mapper event daemon shared library,
libdevmapper-event.

%post -n device-mapper-event-libs -p /sbin/ldconfig

%postun -n device-mapper-event-libs -p /sbin/ldconfig

%package -n device-mapper-event-devel
Summary:    Development libraries and headers for the device-mapper event daemon
License:    LGPLv2
Group:      Development/Libraries
Requires:   device-mapper-event = %{version}-%{release}
Requires:   device-mapper-devel = %{version}-%{release}

%description -n device-mapper-event-devel
This package contains files needed to develop applications that use
the device-mapper event library.

%prep
%setup -q -n LVM2.%{version}
%patch0 -p1 -b .preferred_names
#%patch1 -p1 -b .enable_lvmetad
#%patch2 -p1 -b .udev_no_mpath

%build
%define _default_pid_dir /run
%define _default_dm_run_dir /run
%define _default_run_dir /run/lvm
%define _default_locking_dir /run/lock/lvm
%define _udevdir /lib/udev/rules.d

%configure \
    --prefix=%{_prefix} \
    --with-usrlibdir=%{_libdir} \
    --with-default-dm-run-dir=%{_default_dm_run_dir} \
    --with-default-run-dir=%{_default_run_dir} \
    --with-default-pid-dir=%{_default_pid_dir} \
    --with-default-locking-dir=%{_default_locking_dir} \
    --enable-lvm1_fallback \
    --enable-fsadm \
    --with-pool=internal \
    --enable-write_install \
    --enable-pkgconfig \
    --enable-applib \
    --enable-cmdlib \
    --enable-dmeventd \
    --enable-use_lvmetad \
    --enable-python2-bindings \
    --enable-python3-bindings \
    --enable-blkid_wiping \
    --enable-lvmetad \
    --with-udevdir=%{_udevdir} --enable-udev_sync \
    --with-thin=internal \
    --with-cache=internal \
    --with-cluster=internal --with-clvmd=none


make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
make install_system_dirs DESTDIR=%{buildroot}
make install_systemd_units DESTDIR=%{buildroot}
make install_systemd_generators DESTDIR=%{buildroot}
make install_tmpfiles_configuration DESTDIR=%{buildroot}
cp %{SOURCE1} %{buildroot}/lib/systemd/system/lvm2-activate.service

install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable lvm2-activate.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-lvm2.preset
echo "disable lvm2-monitor.service" >> %{buildroot}%{_libdir}/systemd/system-preset/50-lvm2.preset
echo "disable lvm2-lvmeatd.socket" >> %{buildroot}%{_libdir}/systemd/system-preset/50-lvm2.preset
echo "disable lvm2-lvmeatd.service" >> %{buildroot}%{_libdir}/systemd/system-preset/50-lvm2.preset

%preun
%systemd_preun lvm2-lvmetad.service lvm2-lvmetad.socket lvm2-monitor.service lvm2-activate.service

%post
/sbin/ldconfig
%systemd_post lvm2-lvmetad.service lvm2-lvmetad.socket lvm2-monitor.service lvm2-activate.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart lvm2-lvmetad.service lvm2-lvmetad.socket lvm2-monitor.service lvm2-activate.service

%files  devel
%defattr(-,root,root,-)
%{_libdir}/liblvm2app.so
%{_libdir}/liblvm2cmd.so
%{_libdir}/libdevmapper-event-lvm2.so
%{_includedir}/lvm2app.h
%{_includedir}/lvm2cmd.h
%{_libdir}/pkgconfig/lvm2app.pc


%files libs
%defattr(-,root,root,-)
%{_libdir}/liblvm2app.so.*
%{_libdir}/liblvm2cmd.so.*
%{_libdir}/libdevmapper-event-lvm2.so.*
%dir %{_libdir}/device-mapper
%{_libdir}/device-mapper/libdevmapper-event-lvm2mirror.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2snapshot.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2raid.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2thin.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2vdo.so
%{_libdir}/libdevmapper-event-lvm2mirror.so
%{_libdir}/libdevmapper-event-lvm2snapshot.so
%{_libdir}/libdevmapper-event-lvm2raid.so
%{_libdir}/libdevmapper-event-lvm2thin.so
%{_libdir}/libdevmapper-event-lvm2vdo.so

%files  python-libs
%{python2_sitelib}/*

%files -n  python3-lvm2-libs
%{python3_sitelib}/*

%files -n device-mapper
%defattr(-,root,root,-)
%attr(555, -, -) %{_sbindir}/dmsetup
%{_sbindir}/dmstats
%{_mandir}/man8/dmsetup.8.gz
%{_mandir}/man8/dmstats.8.gz
/lib/udev/rules.d/10-dm.rules
/lib/udev/rules.d/13-dm-disk.rules
/lib/udev/rules.d/95-dm-notify.rules

%files -n device-mapper-devel
%defattr(-,root,root,-)
%{_libdir}/libdevmapper.so
%{_includedir}/libdevmapper.h
%{_libdir}/pkgconfig/devmapper.pc

%files -n device-mapper-libs
%defattr(555,root,root,-)
%{_libdir}/libdevmapper.so.*

%files -n device-mapper-event
%defattr(-,root,root,-)
%attr(555, -, -) %{_sbindir}/dmeventd
%{_mandir}/man8/dmeventd.8.gz
%{_unitdir}/dm-event.socket
%{_unitdir}/dm-event.service

%files -n device-mapper-event-libs
%defattr(555,root,root,-)
%{_libdir}/libdevmapper-event.so.*

%files -n device-mapper-event-devel
%defattr(444,root,root,-)
%{_libdir}/libdevmapper-event.so
%{_includedir}/libdevmapper-event.h
%{_libdir}/pkgconfig/devmapper-event.pc

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/lvm/backup
%dir %{_sysconfdir}/lvm/cache
%dir %{_sysconfdir}/lvm/archive
/lib/udev/rules.d/11-dm-lvm.rules
/lib/udev/rules.d/69-dm-lvm-metad.rules
%{_sbindir}/blkdeactivate
%{_sbindir}/fsadm
%{_sbindir}/lv*
%{_sbindir}/pv*
%{_sbindir}/vg*
%{_mandir}/man5/lvm.conf.5.gz
%{_mandir}/man7/lv*
%{_mandir}/man8/blkdeactivate.8.gz
%{_mandir}/man8/fsadm.8.gz
%{_mandir}/man8/lv*
%{_mandir}/man8/pv*
%{_mandir}/man8/vg*
%{_unitdir}/../system-generators/lvm2-activation-generator
%{_unitdir}/blk-availability.service
%{_unitdir}/lvm2-*
%{_libdir}/systemd/system-preset/50-lvm2.preset
%{_libdir}/tmpfiles.d/lvm2.conf
%dir %{_sysconfdir}/lvm
%attr(644, -, -) %config(noreplace) %{_sysconfdir}/lvm/lvm.conf
%config(noreplace) %{_sysconfdir}/lvm/lvmlocal.conf
%dir %{_sysconfdir}/lvm/profile
%{_sysconfdir}/lvm/profile/*
%ghost %{_sysconfdir}/lvm/cache/.cache


%changelog
*   Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.02.181-1
-   Update to version 2.02.181
*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  2.02.171-3
-   Disabled all lvm services by default
*   Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.02.171-2
-   Added python3 subpackage.
*   Thu May 4  2017 Bo Gan <ganb@vmware.com> 2.02.171-1
-   Update to 2.02.171
*   Wed Dec 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2.02.141-8
-   device-mapper requires systemd.
*   Wed Nov 30 2016 Anish Swaminathan <anishs@vmware.com>  2.02.141-7
-   Start lvmetad socket with the service
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  2.02.141-6
-   Change systemd dependency
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.02.141-5
-   GA - Bump release of all rpms
*   Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 2.02.141-4
-   Adding upgrade support in pre/post/un scripts.
*   Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> 2.02.141-3 
-   Fix post scripts for lvm
*   Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> 2.02.141-2 
-   Adding device mapper event to Requires
*   Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  2.02.116-4
-   Change config file attributes.
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  2.02.116-3
-   Add systemd to Requires and BuildRequires
*   Thu Sep 10 2015 Divya Thaluru <dthaluru@vmware.com> 2.02.116-2
-   Packaging systemd service and configuration files
*   Thu Feb 26 2015 Divya Thaluru <dthaluru@vmware.com> 2.02.116-1
-   Initial version

