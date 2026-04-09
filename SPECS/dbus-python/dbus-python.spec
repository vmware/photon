%global build_if %{photon_subrelease} >= 92

Name:           dbus-python3
Version:        1.4.0
Release:        1%{?dist}
Summary:        Python bindings for D-Bus
Group:          Development/Libraries/Python
Url:            http://www.freedesktop.org/wiki/Software/DBusBindings/

Source0:        https://files.pythonhosted.org/packages/source/d/dbus-python/dbus-python-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python3-devel
BuildRequires:  python3-docutils
BuildRequires:  dbus-devel
BuildRequires:  glib-devel
BuildRequires:  python3-setuptools
BuildRequires:  systemd-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  autoconf-archive
BuildRequires:  libtool

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
%autosetup -n dbus-python-%{version}

%build
NOCONFIGURE=1 ./autogen.sh
%configure PYTHON="%{__python3}"
%make_build %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
cp -r dbus_python*egg-info %{buildroot}%{python3_sitelib}
rm -f %{buildroot}%{python3_sitelib}/*.la
%{py_byte_compile_and_ghost}

%check
make check %{?_smp_mflags}

%files -f %{py_ghost_filelist}
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
* Thu Apr 09 2026 Mukul Sikka <mukul.sikka@broadcom.com> 1.4.0-1
- Update to 1.4.0
* Wed Mar 18 2026 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.3.2-4
- Bump version as a part of python3.14 upgrade
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.3.2-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.3.2-2
- Update release to compile with python 3.11
* Tue Nov 01 2022 Susant Sahani <ssahani@vmware.com> 1.3.2-1
- version bump
* Mon Dec 14 2020 Susant Sahani <ssahani@vmware.com> 1.2.16-2
- Add build requires
* Thu Mar 19 2020 Tapas Kundu <tkundu@vmware.com> 1.2.16-1
- Initial release
