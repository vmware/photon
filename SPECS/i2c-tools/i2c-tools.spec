Summary:        A set of I2C tools for Linux Kernel
Name:           i2c-tools
Version:        4.3
Release:        1%{?dist}
License:        LGPL-2.1+
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://i2c.wiki.kernel.org/index.php/I2C_Tools
Source0:        https://www.kernel.org/pub/software/utils/i2c-tools/%{name}-%{version}.tar.xz
%define sha512 %{name}-%{version}=8a6cc12d927d6291b9baf407bc15807280539a7048ec5c2edf77414432eab43b28353c42bc0e45b7b481502aa4c5588def08f130d97fc275f635d1f77488f501

%description
This package contains a heterogeneous set of I2C tools for Linux Kernelas well as an I2C library.
Various tools are included in this package with different catagories:
eeprom, eeprog, eepromer, py-smbus, tools that rely on "i2c-dev" kernel driver.

%package    devel
Summary:    Header and development files for zlib
Requires:   %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files.

%prep
%autosetup

%build
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} PREFIX=%{_prefix} %{?_smp_mflags} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/libi2c.so.0*
%{_mandir}/man1/*.1.gz
%{_mandir}/man3/*.3.gz
%{_mandir}/man8/*.8.gz

%files devel
%dir %{_includedir}/i2c
%{_includedir}/i2c/smbus.h
%{_libdir}/libi2c.a
%{_libdir}/libi2c.so

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 4.3-1
-   Automatic Version Bump
*   Tue Sep 22 2020 Gerrit Photon <photon-checkins@vmware.com> 4.2-1
-   Automatic Version Bump
*   Wed Feb 27 2019 Ankit Jain <ankitja@vmware.com> 4.1-1
-   Initial version.
