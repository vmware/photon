Summary:        The lm_sensors package provides user-space support for the hardware monitoring drivers in the Linux kernel.
Name:           lm-sensors
Version:        3.5.0
Release:        2%{?dist}
License:        GPLv2
URL:            https://github.com/lm-sensors/lm-sensors
Group:          System Drivers
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://ftp.gwdg.de/pub/linux/misc/lm-sensors/%{name}-%{version}.tar.gz
%define sha1    lm-sensors=3d1b3b82d62daeec1f151eaf993c61dc3cf21a6b
BuildRequires:  gcc
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  make
BuildRequires:  bison
BuildRequires:  glibc-devel
BuildRequires:  libgcc-devel
BuildRequires:  which
Requires:       perl
Requires:       linux >= 4.9.180-2

%description
The lm_sensors package provides user-space support for the hardware monitoring drivers in the Linux kernel.
This is useful for monitoring the temperature of the CPU and adjusting the performance of some hardware (such as cooling fans).

%package   devel
Summary:   lm-sensors devel
Group:     Development/Libraries
Requires:  lm-sensors = %{version}-%{release}

%description devel
lm-sensors devel

%package   doc
Summary:   lm-sensors docs
Group:     Development/Libraries
Requires:  lm-sensors = %{version}-%{release}

%description doc
Documentation for lm-sensors.

%prep
%setup -q -n %{name}-3-5-0

%build

make all %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/lib
mkdir -p %{buildroot}/usr/share
make PREFIX=%{buildroot}/usr        \
     BUILD_STATIC_LIB=0 \
     MANDIR=%{buildroot}/usr/share/man install &&

install -v -m755 -d %{buildroot}/usr/share/doc/%{name}-%{version} &&
cp -rv              README INSTALL doc/* \
                    %{buildroot}/usr/share/doc/%{name}-%{version}
%check

%post
/sbin/modprobe i2c-dev

%postun
/sbin/modprobe -r i2c-dev

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libsensors.so.5
%{_libdir}/libsensors.so.5.0.0
%{_sbindir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libsensors.so

%files doc
%defattr(-,root,root)
%{_docdir}/*
%{_mandir}/*

%changelog
* Wed Jun 19 2019 Tapas Kundu <tkundu@vmware.com> 3.5.0-2
- Added main pkg as requires to devel and doc
* Fri May 24 2019 Tapas Kundu <tkundu@vmware.com> 3.5.0-1
- Initial packaging with Photon OS.
