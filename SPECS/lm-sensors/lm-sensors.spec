Summary:        The lm_sensors package provides user-space support for the hardware monitoring drivers in the Linux kernel.
Name:           lm-sensors
Version:        3.6.0
Release:        1%{?dist}
License:        GPLv2
URL:            https://github.com/lm-sensors/lm-sensors/releases
Group:          System Drivers
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/lm-sensors/lm-sensors/archive/%{name}-%{version}.tar.gz
%define sha1    lm-sensors=2ef03242b62d70523919d06859503f12feb9f7d4
BuildRequires:  gcc
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  make
BuildRequires:  bison
BuildRequires:  glibc-devel
BuildRequires:  libgcc-devel
BuildRequires:  which
Requires:       perl
Requires:       linux >= 4.19.52-2

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
%setup -qn %{name}-3-6-0

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
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.6.0-1
- Automatic Version Bump
* Thu Jun 20 2019 Tapas Kundu <tkundu@vmware.com> 3.5.0-1
- Initial packaging with Photon OS.
