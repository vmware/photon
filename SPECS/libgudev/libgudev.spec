Summary:        A library providing GObject bindings for libudev
Name:           libgudev
Version:        232
Release:        2%{?dist}
License:        LGPL2.1
URL:            https://git.gnome.org/browse/libgudev/
Source0:        https://git.gnome.org/browse/%{name}/snapshot/%{name}-%{version}.tar.xz
%define sha512 libgudev=f648a41e2a6af7e26634c7cc259fdc47bb6e6ffb329324d157f340e42928e28c2059a0e923b9b0aaecd1ee3ecafbc7b55e5652f1f77bc1b88367b97057a1bedc
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
BuildRequires:  glib >= 2.22.0
BuildRequires:  glib-devel
BuildRequires:  gnome-common
BuildRequires:  gobject-introspection
BuildRequires:  gtk-doc
BuildRequires:  pkg-config
BuildRequires:  systemd-devel
BuildRequires:  which
Requires:       systemd
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
%autosetup -p1

%build
%configure  --disable-umockdev
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make -k check %{?_smp_mflags}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gudev-1.0.pc

%changelog
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 232-2
- Remove .la files
* Sun Sep 30 2018 Bo Gan <ganb@vmware.com> 232-1
- Update to 232
* Mon Apr 10 2017 Harish Udaiya kumar <hudaiyakumar@vmware.com> 231-1
- Updated to version 231.
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  230-4
- Change systemd dependency
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 230-3
- GA - Bump release of all rpms
* Thu Aug 13 2015 Vinay Kulkarni <kulkarniv@vmware.com> 230-2
- Split header files into devel package.
* Tue Aug 11 2015 Vinay Kulkarni <kulkarniv@vmware.com> 230-1
- Add libgudev v230
