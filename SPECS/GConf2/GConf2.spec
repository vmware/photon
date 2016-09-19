Summary:        GConf2
Name:           GConf2
Version:        3.2.6
Release:        1%{?dist}
License:        GPL2+
URL:            http://download.gnome.org/sources/GConf/3.2/
Source0:        http://download.gnome.org/sources/GConf/3.2/GConf-%{version}.tar.xz
%define sha1    GConf=a90d3ac08dc454f927c8d3024f52d4d57e3ff613
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
#BuildArch:     noarch
BuildRequires:  glib-devel
BuildRequires:  libxml2-devel
BuildRequires:  dbus-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  libxslt-devel
BuildRequires:  intltool
BuildRequires:  autoconf automake libtool
%description
GConf is a system for storing application preferences. It is intended for user preferences; not configuration of something like Apache, or arbitrary data storage.
%prep
%setup -qn GConf-%{version}
%build
./configure --prefix=/usr \
            --sysconfdir=/etc \
            --disable-orbit \
            --disable-static
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%exclude %{_libdir}/debug
%exclude /usr/src/debug
%{_sysconfdir}/*
/usr/*

%changelog
*   Tue Sep 6 2016 Xiaolin Li <xiaolinl@vmware.com> 3.2.6-1
-   Initial build. First version
