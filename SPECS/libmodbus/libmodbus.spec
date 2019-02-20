Summary:	Modbus library for linux
Name:		libmodbus
Version:	3.0.6
Release:	1%{?dist}
License:	LGPLv2+
URL:		http://www.libmodbus.org/
Group:		Development/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/downloads/stephane/%{name}/%{name}-%{version}.tar.gz
%define sha1 libmodbus=32002975fab4b9882a0b0d4d6095dcf90b5390ce

%description
libmodbus is a C library designed to provide a fast and robust implementation of
the Modbus protocol. This package contains the libmodbus shared library.

%package        devel
Summary:        Development files node
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The libmodbus-devel package contains libraries, header files and documentation
for developing applications that use libmodbus.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS MIGRATION NEWS COPYING* README.rst
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/modbus/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
%{_libdir}/*.la
%{_mandir}/*

%changelog
*    Thu Feb 14 2019 Him Kalyan Bordoloi <bordoloih@vmware.com> 3.0.6-1
-    Initial build added for Photon.
