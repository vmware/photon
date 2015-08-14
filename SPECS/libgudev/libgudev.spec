Summary:        A library providing GObject bindings for libudev
Name:           libgudev
Version:        230
Release:        2%{?dist}
License:        LGPL2.1
URL:            https://git.gnome.org/browse/libgudev/
Source0:        https://git.gnome.org/browse/%{name}/snapshot/%{name}-%{version}.tar.xz
%define sha1 libgudev=2f39afc6a9cde5138140d1b03fa438b8f4f59ca0
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
BuildRequires:  glib >= 2.22.0
BuildRequires:  glib-devel
BuildRequires:  gnome-common
BuildRequires:  gobject-introspection
BuildRequires:  gtk-doc
BuildRequires:  pkg-config
BuildRequires:  systemd
BuildRequires:  which
Requires:       systemd
Provides:       libgudev-1.0.so=0-64
Distribution:   Photon

%description
This is libgudev, a library providing GObject bindings for libudev. It
used to be part of udev, and now is a project on its own.

%package devel
Summary:        Header and development files for libgudev
Requires:       %{name} = %{version}
Requires:       glib-devel

%description devel
libgudev-devel package contains header files for building gudev applications.

%prep
%setup -q
./autogen.sh

%build
./configure \
        --prefix=%{_prefix}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libgudev-1.0.so.0.2.0

%files devel
%{_includedir}/gudev-1.0/gudev/gudev.h
%{_includedir}/gudev-1.0/gudev/gudevclient.h
%{_includedir}/gudev-1.0/gudev/gudevdevice.h
%{_includedir}/gudev-1.0/gudev/gudevenumerator.h
%{_includedir}/gudev-1.0/gudev/gudevenums.h
%{_includedir}/gudev-1.0/gudev/gudevenumtypes.h
%{_includedir}/gudev-1.0/gudev/gudevtypes.h
%{_libdir}/libgudev-1.0.la
%{_libdir}/libgudev-1.0.so
%{_libdir}/libgudev-1.0.so.0
%{_libdir}/pkgconfig/gudev-1.0.pc

%changelog
*       Thu Aug 13 2015 Vinay Kulkarni <kulkarniv@vmware.com> 230-2
-       Split header files into devel package.
*       Tue Aug 11 2015 Vinay Kulkarni <kulkarniv@vmware.com> 230-1
-       Add libgudev v230

