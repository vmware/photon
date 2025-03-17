Name:           gpsd
Version:        3.25
Release:        3%{?dist}
Summary:        Service daemon for mediating access to a GPS
Group:          System Environment
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://gpsd.gitlab.io/gpsd

Source0:        https://download-mirror.savannah.gnu.org/releases/%{name}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  dbus-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  ncurses-devel
BuildRequires:  xmlto
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  scons
BuildRequires:  python3-pygobject
BuildRequires:  cairo
BuildRequires:  fontconfig-devel
BuildRequires:  freetype2-devel
BuildRequires:  python3-pyserial
BuildRequires:  bluez-devel
BuildRequires:  systemd-devel
BuildRequires:  libusb-devel

Requires: %{name}-libs = %{version}-%{release}
Requires: dbus
Requires: systemd
Requires: libical
Requires: bluez
Requires: libusb
Requires: util-linux-libs
Requires: ncurses-libs
Requires: libcap
Requires: libgpg-error
Requires: xz-libs
Requires: glibc

%description
gpsd is a service daemon that mediates access to a GPS sensor
connected to the host computer by serial or USB interface, making its
data on the location/course/velocity of the sensor available to be
queried on TCP port 2947 of the host computer.  With gpsd, multiple
GPS client applications (such as navigational and wardriving software)
can share access to a GPS without contention or loss of data.  Also,
gpsd responds to queries with a format that is substantially easier to
parse than NMEA 0183.

%package libs
Summary: Client libraries in C for talking to a running gpsd or GPS
Requires: bluez

%description libs
This package contains the gpsd libraries that manage access
to a GPS for applications.

%package -n python3-%{name}
Summary: Python libraries and modules for use with gpsd
Requires: %{name}-libs = %{version}-%{release}
Requires: python3
Provides: python-%{name}
BuildArch: noarch

%description -n python3-%{name}
This package contains the python3 modules that manage access to a GPS for
applications, and commonly useful python applications for use with gpsd.

%package devel
Summary: Development files for the gpsd library
Requires: %{name}-libs = %{version}-%{release}

%description devel
This package provides C header files for the gpsd shared libraries that
manage access to a GPS for applications

%package clients
Summary: Clients for gpsd
Requires: python3-%{name} = %{version}-%{release}
Requires: python3-pyserial
Requires: python3-pygobject
Requires: %{name}-libs = %{version}-%{release}

%description clients
xgps is a simple test client for gpsd with an X interface. It displays
current GPS position/time/velocity information and (for GPSes that
support the feature) the locations of accessible satellites.

xgpsspeed is a speedometer that uses position information from the GPS.
It accepts an -h option and optional argument as for gps, or a -v option
to dump the package version and exit. Additionally, it accepts -rv
(reverse video) and -nc (needle color) options.

cgps resembles xgps, but without the pictorial satellite display.  It
can run on a serial terminal or terminal emulator.

gpsfake can feed data from files to simulate data coming from many
different gps devices.

%prep
%autosetup -p1

%build
export CCFLAGS="%{optflags}"
export LINKFLAGS="-lm"

# breaks with %{_smp_mflags}
scons \
    bindir=%{_bindir} \
    build packaging \
    dbus_export=yes \
    debug=yes \
    docdir=%{_docdir} \
    icondir=%{_datadir}/%{name} \
    includedir=%{_includedir} \
    leapfetch=no \
    libdir=%{_libdir} \
    libQgpsmm=no \
    manbuild=no \
    pkgconfigdir=%{_libdir}/pkgconfig \
    prefix=%{_prefix} \
    python_libdir=%{python3_sitearch} \
    python_shebang="%{python3}" \
    release=%{release} \
    sbindir=%{_sbindir} \
    sysconfdif=%{_sysconfdir} \
    systemd=yes \
    target_python=python3 \
    udevdir=$(dirname %{_udevrulesdir}) \
    unitdir=%{_unitdir}

%install
# avoid rebuilding
export CCFLAGS="%{optflags}"
export LINKFLAGS="-lpthread"

DESTDIR=%{buildroot} scons install systemd_install udev-install

# use the old name for udev rules
mv %{buildroot}%{_udevrulesdir}/{25,99}-%{name}.rules

%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -p -m 0644 packaging/rpm/%{name}.sysconfig \
    %{buildroot}%{_sysconfdir}/sysconfig/%{name}

# Delete the .desktop files (no GUI in Photon)
rm -f packaging/X11/xgpsspeed.desktop packaging/X11/xgps.desktop

# Don't package doc/man files
rm -rf INSTALL.adoc TODO %{buildroot}%{_datadir}/doc %{buildroot}/%{_mandir}/man*

# Missed in scons install
%{__install} -p -m 0755 gpsinit %{buildroot}%{_sbindir}

%post
%systemd_post %{name}.service %{name}.socket

%preun
%systemd_preun %{name}.service %{name}.socket

%postun
# Don't restart the service
%systemd_postun %{name}.service %{name}.socket

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%exclude %{_datadir}/snmp/mibs/%{name}/GPSD-MIB
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_sbindir}/%{name}
%{_sbindir}/gpsdctl
%{_sbindir}/gpsinit
%{_bindir}/gpsdebuginfo
%{_bindir}/gpsmon
%{_bindir}/gpssnmp
%{_bindir}/gpsctl
%{_bindir}/ntpshmmon
%{_bindir}/ppscheck
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket
%{_unitdir}/gpsdctl@.service
%{_udevrulesdir}/*.rules

%files libs
%defattr(-,root,root)
%{_libdir}/libgps.so.*
%{_libdir}/libgpsdpacket.so.*

%files -n python3-%{name}
%defattr(-,root,root)
%{_bindir}/gpsprof
%{python3_sitearch}/gps*
%{python3_sitearch}/gps/fake*

%files devel
%defattr(-,root,root)
%{_libdir}/libgps.so
%{_libdir}/libgpsdpacket.so
%{_libdir}/pkgconfig/libgps.pc
%{_includedir}/gps.h
%{_includedir}/libgpsmm.h

%files clients
%defattr(-,root,root)
%{_bindir}/cgps
%{_bindir}/gegps
%{_bindir}/gps2udp
%{_bindir}/gpscat
%{_bindir}/gpscsv
%{_bindir}/gpsdecode
%{_bindir}/gpspipe
%{_bindir}/gpsplot
%{_bindir}/gpsrinex
%{_bindir}/gpssubframe
%{_bindir}/gpxlogger
%{_bindir}/lcdgps
%{_bindir}/xgps
%{_bindir}/xgpsspeed
%{_bindir}/gpsfake
%{_bindir}/ubxtool
%{_bindir}/zerk
%dir %{_datadir}/%{name}
%exclude %{_datadir}/%{name}/gpsd-logo.png

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 3.25-3
- Release bump for SRP compliance
* Tue Apr 02 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 3.25-2
- Version Bump up to consume bluez v5.71
* Tue Jun 06 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 3.25-1
- Initial addition to Photon. Adapted from provided spec file
- in the gpsd gitlab repository.
