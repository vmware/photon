Summary:        A library which allows userspace access to USB devices
Name:           libusb
Version:        1.0.26
Release:        1%{?dist}
License:        LGPLv2+
URL:            http://sourceforge.net/projects/libusb/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source:         http://downloads.sourceforge.net/libusb/libusb-%{version}.tar.bz2
%define sha512  libusb=fcdb85c98f21639668693c2fd522814d440972d65883984c4ae53d0555bdbdb7e8c7a32199cd4b01113556a1eb5be7841b750cc73c9f6bda79bfe1af80914e71
BuildRequires:  systemd-devel
Requires:       systemd

%description
This package provides a way for applications to access USB devices.

%package        devel
Summary:        Development files for libusb
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description    devel
This package contains the header files, libraries and documentation needed to
develop applications that use libusb.

%prep
%autosetup

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} %{?_smp_mflags} install

%check
pushd tests
make %{?_smp_mflags} -k check
./stress
popd

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libdir}/libusb*.so.*

%files devel
%{_includedir}/*
%{_libdir}/libusb*.so
%{_libdir}/libusb*.la
%{_libdir}/pkgconfig/*

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.0.26-1
-   Automatic Version Bump
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.0.24-1
-   Automatic Version Bump
*   Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.0.23-1
-   Automatic Version Bump
*   Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 1.0.22-1
-   Update to version 1.0.22
*   Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com>  1.0.21-1
-   Upgrading version to 1.0.21
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.0.20-4
-   Change systemd dependency
*   Tue Jul 12 2016 Xiaolin Li <xiaolinl@vmware.com>  1.0.20-3
-   Build libusb single threaded.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.20-2
-   GA - Bump release of all rpms
*   Thu May 05 2016 Nick Shi <nshi@vmware.com> 1.0.20-1
-   Initial version.
