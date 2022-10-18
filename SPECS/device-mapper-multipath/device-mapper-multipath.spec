Summary:        Provide tools to manage multipath devices
Name:           device-mapper-multipath
Version:        0.9.0
Release:        1%{?dist}
License:        GPL+
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/bmarzins/rh-multipath-tools
Source0:        rh-multipath-tools-%{version}.tar.gz
%define sha512  rh-multipath-tools=6c417f6d1d116fa43bedb9f77769ece9cbb7b35b78a9b3558c41df2360e52a65a07314b12ab7e4a7bbc867b9755250de9db96a2f7eb4a6a37f0b0b3f0bbc840e
BuildRequires:  userspace-rcu-devel
BuildRequires:  libaio-devel
BuildRequires:  device-mapper-devel
BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
BuildRequires:  systemd-devel
BuildRequires:  json-c-devel
Requires:       userspace-rcu
Requires:       libaio
Requires:       device-mapper
Requires:       libselinux
Requires:       libsepol
Requires:       readline
Requires:       ncurses
Requires:       kpartx = %{version}-%{release}

%description
Device-mapper-multipath provides tools to manage multipath devices by
instructing the device-mapper multipath kernel module what to do.

%package -n     kpartx
Summary:        Partition device manager for device-mapper devices
Requires:       device-mapper
%description -n kpartx
kpartx manages partition creation and removal for device-mapper devices.

%package        devel
Summary:        Development libraries and headers for %{name}
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -n multipath-tools-%{version}

%build
make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot} \
	SYSTEMDPATH=/lib \
	bindir=%{_sbindir} \
	syslibdir=%{_libdir} \
	libdir=%{_libdir}/multipath \
	pkgconfdir=%{_libdir}/pkgconfig
install -vd %{buildroot}/etc/multipath

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_sbindir}/mpathpersist
%{_sbindir}/multipath
%{_sbindir}/multipathd
/lib/udev/rules.d/*
/lib64/*.so
/lib64/*.so.*
%{_libdir}/*.so
%{_libdir}/*.so.*
%{_libdir}/multipath/*.so
/lib/systemd/system/multipathd.service
/lib/systemd/system/multipathd.socket
/lib/modules-load.d/multipath.conf
%{_mandir}/man5/*
%{_mandir}/man8/mpathpersist.8.gz
%{_mandir}/man8/multipath.8.gz
%{_mandir}/man8/multipathd.8.gz

%files devel
%defattr(-,root,root,-)
%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files -n kpartx
%defattr(-,root,root,-)
%{_sbindir}/kpartx
/lib/udev/kpartx_id
%{_mandir}/man8/kpartx.8.gz

%changelog
*   Sun Sep 18 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.9.0-1
-   Upgrade to version 0.9.0
*   Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 0.8.6-1
-   Automatic Version Bump
*   Wed Oct 07 2020 Shreenidhi Shedi <sshedi@vmware.com> 0.8.4-1
-   Upgrade to version 0.8.4
*   Tue Aug 18 2020 Michelle Wang <michellew@vmware.com> 0.8.3-2
-   Fix how to call json_object_object_get_ex in ./libdmmp/libdmmp_private.h
-   due to json-c 0.15 update json_object_object_get_ex return value
*   Wed Apr 08 2020 Susant Sahani <ssahani@vmware.com> 0.8.3-1
-   Update to 0.8.3
*   Thu Dec 06 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 0.7.3-3
-   Make device-mapper a runtime dependency of kpartx.
*   Wed Sep 26 2018 Anish Swaminathan <anishs@vmware.com>  0.7.3-2
-   Remove rados dependency
*   Wed Oct 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.7.3-1
-   Update to 0.7.3
*   Tue May 9  2017 Bo Gan <ganb@vmware.com> 0.7.1-1
-   Update to 0.7.1
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  0.5.0-3
-   Change systemd dependency
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.5.0-2
-   GA - Bump release of all rpms
*   Mon Jun 22 2015 Divya Thaluru <dthaluru@vmware.com> 0.5.0-1
-   Initial build. First version
