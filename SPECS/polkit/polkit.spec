Summary:       A toolkit for defining and handling authorizations.
Name:          polkit
Version:       0.113
Release:       2%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       LGPLv2+
URL:           https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html
Source0:       https://www.freedesktop.org/software/polkit/releases/%{name}-%{version}.tar.gz
Distribution:  Photon
BuildRequires: autoconf
BuildRequires: expat-devel
BuildRequires: glib-devel
BuildRequires: gobject-introspection
BuildRequires: intltool >= 0.40.0
BuildRequires: js-devel
BuildRequires: Linux-PAM-devel
BuildRequires: systemd-devel
Requires:      expat
Requires:      glib
Requires:      js
Requires:      Linux-PAM
Requires:      systemd
%define sha1 polkit=ef855c2d04184dceb38e0940dc7bec9cc3da415c

%description
polkit provides an authorization API intended to be used by privileged programs
(“MECHANISMS”) offering service to unprivileged programs (“SUBJECTS”) often
through some form of inter-process communication mechanism

%package devel
Summary: polkit development headers and libraries
Group: Development/Libraries
Requires: polkit = %{version}-%{release}

%description devel
header files and libraries for polkit

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --datadir=%{_datarootdir} \
    --sysconfdir=%{_sysconfdir} \
    --enable-libsystemd-login=yes \
    --with-systemdsystemunitdir=%{_libdir}/systemd/system
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
# Disable check. It requires dbus - not available in chroot/container.

%pre
getent group polkitd > /dev/null || groupadd -fg 27 polkitd &&
getent passwd polkitd > /dev/null || \
    useradd -c "PolicyKit Daemon Owner" -d /etc/polkit-1 -u 27 \
        -g polkitd -s /bin/false polkitd

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/pk*
%{_libdir}/lib%{name}-*.so.*
%{_libdir}/polkit-1/polkit-agent-helper-1
%{_libdir}/polkit-1/polkitd
%{_libdir}/systemd/system/polkit.service
%{_datarootdir}/dbus-1/system-services/org.freedesktop.PolicyKit1.service
%{_datarootdir}/locale/*
%{_datarootdir}/polkit-1/actions/*.policy
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%{_sysconfdir}/pam.d/polkit-1
%{_sysconfdir}/polkit-1/rules.d/50-default.rules

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}-1/
%{_libdir}/lib%{name}-*.a
%{_libdir}/lib%{name}-*.so
%{_libdir}/pkgconfig/*.pc

%changelog
*   Thu Oct 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.113-2
-   Initial version of polkit for PhotonOS.
*   Wed Oct 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.113-1
-   Upgrade to 0.113-1
*   Fri May 22 2015 Alexey Makhalov <amakhalov@vmware.com> 0.112-1
-   initial version
