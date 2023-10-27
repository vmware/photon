%global __python3 \/usr\/bin\/python3

Name:           dbus-python3
Version:        1.2.16
Release:        5%{?dist}
Summary:        Python bindings for D-Bus
License:        MIT
Group:          Development/Libraries/Python
Url:            http://www.freedesktop.org/wiki/Software/DBusBindings/
Source0:        http://dbus.freedesktop.org/releases/dbus-python/dbus-python-%{version}.tar.gz
%define         sha512 dbus-python=e76c00c5fd3fe6884e4c24f258987fd3b80d21bd4e0f96aa8fda152078a860b62321324f6efcbfe7226d5ab2521a14b5bda7cf2468d2cae5f376c124a71aa05c
Patch0:         fix-deprecated-collections.patch
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-docutils
BuildRequires:  dbus-devel
BuildRequires:  glib-devel >= 2.68.4
BuildRequires:  python3-setuptools
BuildRequires:  systemd-devel

Requires:       python3-xml
Requires:       dbus

%description
D-Bus python bindings for use with python programs.

%package -n     dbus-python3-devel
Summary:        Python bindings for D-Bus
Group:          Development/Libraries/Python
Requires:       %{name} = %{version}
Requires:       dbus-devel

%description -n dbus-python3-devel
Developer files for Python bindings for D-Bus.

%prep
%autosetup -p1 -n dbus-python-%{version}

%build
%configure PYTHON="%{__python3}"
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
cp -r dbus_python*egg-info %{buildroot}%{python3_sitelib}
rm -f %{buildroot}%{python3_sitelib}/*.la

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%doc NEWS
%license COPYING
%{python3_sitelib}/*.so
%{python3_sitelib}/dbus/
%{python3_sitelib}/dbus_python*egg-info

%files devel
%defattr(-,root,root)
%doc README ChangeLog doc/API_CHANGES.txt doc/tutorial.txt
%{_includedir}/dbus-1.0/dbus/dbus-python.h
%{_libdir}/pkgconfig/dbus-python.pc

%changelog
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.2.16-5
- Bump version as part of glib upgrade
* Thu Jan 13 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.2.16-4
- Add patch to replace deprecated Sequence from collection to collections.abc
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 1.2.16-3
- Bump up to compile with python 3.10
* Mon Dec 14 2020 Susant Sahani <ssahani@vmware.com> 1.2.16-2
- Add build requires
* Thu Mar 19 2020 Tapas Kundu <tkundu@vmware.com> 1.2.16-1
- Initial release
