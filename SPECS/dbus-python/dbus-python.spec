%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%global __python3 \/usr\/bin\/python3

Name:           dbus-python3
Version:        1.2.16
Release:        2%{?dist}
Summary:        Python bindings for D-Bus
License:        MIT
Group:          Development/Libraries/Python
Url:            http://www.freedesktop.org/wiki/Software/DBusBindings/
Source0:        http://dbus.freedesktop.org/releases/dbus-python/dbus-python-%{version}.tar.gz
%define         sha1 dbus-python=de05308c75baa2ce5434de73d60428c005ac0cc1
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-docutils
BuildRequires:  dbus-devel
BuildRequires:  glib-devel
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
%setup -q -n dbus-python-%{version}

%build
%configure PYTHON="%{__python3}"
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
cp -r dbus_python*egg-info %{buildroot}%{python3_sitelib}
rm -f %{buildroot}%{python3_sitelib}/*.la

%check
make check

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
*   Mon Dec 14 2020 Susant Sahani <ssahani@vmware.com> 1.2.16-2
-   Add build requires
*   Thu Mar 19 2020 Tapas Kundu <tkundu@vmware.com> 1.2.16-1
-   Initial release
