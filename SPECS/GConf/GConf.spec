Summary:        configuration database system used by many GNOME applications
Name:           GConf
Version:        3.2.6
Release:        3%{?dist}
License:        LGPLv2+
URL:            http://gnome.org
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnome.org/pub/gnome/sources/%{name}/3.2/%{name}-%{version}.tar.xz
%define sha512 %{name}=35f5f659f9d03f7531a7102adacbda0eb310d8a55a831c768c91a82e07dae21247726e00e0e411f63b1de9ade0f042ded572a3ea4a4b2ad3135231f344540b58

BuildRequires:  intltool
BuildRequires:  shadow
BuildRequires:  libxml2-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  polkit-devel

Requires:       libxml2
Requires:       dbus-glib
Requires:       polkit

Requires(post): grep

%description
The GConf package contains a configuration database system used by many GNOME applications.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Requires:       libxml2-devel
Requires:       dbus-glib-devel
Requires:       polkit-devel

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure \
        --disable-orbit \
        --enable-defaults-service \
        --disable-static

%make_build

%install
%make_install %{?_smp_mflags}
ln -s gconf.xml.defaults %{buildroot}%{_sysconfdir}/gconf/gconf.xml.system

%post
/sbin/ldconfig
if [ $1 -gt 1 ]; then
  if ! fgrep -q gconf.xml.system %{_sysconfdir}/gconf/2/path; then
    sed -i -e 's@xml:readwrite:$(HOME)/.gconf@&\n\n# Location for system-wide settings.\nxml:readonly:/etc/gconf/gconf.xml.system@' %{_sysconfdir}/gconf/2/path
  fi
fi

%postun -p /sbin/ldconfig

%check
cd tests
make %{?_smp_mflags}
fns=$(find -name 'test*' -executable -maxdepth 1)
for fn in $fns; do
  $fn || :
done

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}
%{_sysconfdir}/
%{_libexecdir}/
%{_libdir}/*.so.*
%{_libdir}/GConf
%{_libdir}/gio

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/
%{_datadir}

%changelog
*   Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 3.2.6-3
-   Bump version as a part of libxml2 upgrade
*   Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.2.6-2
-   Bump version as a part of libxml2 upgrade
*   Thu Dec 15 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2.6-1
-   Automatic Version Bump
*   Wed Nov 15 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.2.5-2
-   Updated build requires
*   Thu Jun 4 2015 Alexey Makhalov <amakhalov@vmware.com> 3.2.5-1
-   initial version
