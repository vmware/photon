Summary:        A library providing GObject bindings for libudev
Name:           libgudev
Version:        234
Release:        3%{?dist}
License:        LGPL2.1
URL:            https://git.gnome.org/browse/libgudev/
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://git.gnome.org/browse/%{name}/snapshot/%{name}-%{version}.tar.xz
%define sha512 libgudev=cb01906d532b05cf8f69acdf80a8f05fbd4863fd98e88928b491e3657e60844f7ae6ca903ddd773fbea37268ff85d12719de47fd92a2f18b98fa2dbfe85e8151

BuildRequires:  glib >= 2.68.4
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  gnome-common
BuildRequires:  gobject-introspection
BuildRequires:  gtk-doc
BuildRequires:  pkg-config
BuildRequires:  systemd-devel
BuildRequires:  which

Requires:       systemd

%description
This is libgudev, a library providing GObject bindings for libudev. It
used to be part of udev, and now is a project on its own.

%package devel
Summary:        Header and development files for libgudev
Requires:       %{name} = %{version}-%{release}
Requires:       glib-devel >= 2.68.4

%description devel
libgudev-devel package contains header files for building gudev applications.

%prep
%autosetup -p1

%build
%configure  --disable-umockdev
make %{?_smp_mflags}

%install
%make_install %{?_smp_mflags}

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
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 234-3
- Bump version as part of glib upgrade
* Sun Oct 02 2022 Shreenidhi Shedi <sshedi@vmware.com> 234-2
- Remove .la files
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 234-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 233-1
- Automatic Version Bump
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
