Summary:       A toolkit for defining and handling authorizations.
Name:          polkit
Version:       0.120
Release:       5%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       LGPLv2+
URL:           http://www.freedesktop.org/wiki/Software/polkit
Distribution:  Photon

Source0: https://gitlab.freedesktop.org/polkit/polkit/-/archive/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=db072769439d5e17d0eed681e7b94251b77828c1474b40fe40b94293903a64333e7fa17515a3270648691f04a1374d8b404405ead6abf292a8eb8483164adc46

Patch0: CVE-2021-4034.patch
Patch1: CVE-2021-4115.patch

BuildRequires: autoconf
BuildRequires: expat-devel
BuildRequires: glib-devel >= 2.68.4
BuildRequires: gobject-introspection
BuildRequires: intltool
BuildRequires: mozjs-devel
BuildRequires: Linux-PAM-devel
BuildRequires: systemd-devel

Requires: mozjs
Requires: expat
Requires: glib >= 2.68.4
Requires: Linux-PAM
Requires: systemd
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel

%description
polkit provides an authorization API intended to be used by privileged programs
(“MECHANISMS”) offering service to unprivileged programs (“SUBJECTS”) often
through some form of inter-process communication mechanism

%package devel
Summary: polkit development headers and libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
header files and libraries for polkit

%prep
%autosetup -p1

%build
%configure \
    --enable-libsystemd-login=yes \
    --with-systemdsystemunitdir=%{_unitdir}

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_sysconfdir}/pam.d
cat > %{buildroot}%{_sysconfdir}/pam.d/%{name}-1 << "EOF"
# Begin /etc/pam.d/polkit-1

auth     include        system-auth
account  include        system-account
password include        system-password
session  include        system-session

# End /etc/pam.d/polkit-1
EOF

%pre
getent group polkitd > /dev/null || groupadd -fg 27 polkitd
getent passwd polkitd > /dev/null || \
  useradd -c "PolicyKit Daemon Owner" -d %{_sysconfdir}/%{name}-1 -u 27 \
    -g polkitd -s /bin/false polkitd

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
  systemctl stop %{name}
fi

%files
%defattr(-,root,root)
%{_bindir}/pk*
%{_libdir}/lib%{name}-*.so.*
%{_libdir}/%{name}-1/%{name}-agent-helper-1
%{_libdir}/%{name}-1/polkitd
%{_libdir}/systemd/system/%{name}.service
%{_datarootdir}/dbus-1/system-services/org.freedesktop.PolicyKit1.service
%{_datarootdir}/locale/*
%{_datarootdir}/%{name}-1/actions/*.policy
%{_datarootdir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%{_sysconfdir}/pam.d/%{name}-1
%{_sysconfdir}/%{name}-1/rules.d/50-default.rules
%{_datadir}/gettext/its

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}-1/
%{_libdir}/lib%{name}-*.a
%{_libdir}/lib%{name}-*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.120-5
- Bump version as part of glib upgrade
* Tue Aug 29 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.120-4
- Bump version as a part of mozjs upgrade
* Mon Feb 07 2022 Siju Maliakkal <smaliakkal@vmware.com> 0.120-3
- Fix for CVE-2021-4115
* Thu Jan 20 2022 Siju Maliakkal <smaliakkal@vmware.com> 0.120-2
- Fix for CVE-2021-4034
* Mon Nov 15 2021 Prashant S Chauhan <psinghchauha@vmware.com> 0.120-1
- Update to version 0.120, to compile with python 3.10
* Wed May 26 2021 Siju Maliakkal <smaliakkal@vmware.com> 0.118-2
- Fix CVE-2021-3560
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 0.118-1
- Automatic Version Bump
* Tue Aug 25 2020 Ankit Jain <ankitja@vmware.com> 0.117-2
- This version of polkit build requires specific mozjs version
* Thu Aug 13 2020 Ankit Jain <ankitja@vmware.com> 0.117-1
- Upgraded to 0.117
* Sat Oct 26 2019 Ankit Jain <ankitja@vmware.com> 0.116-1
- Upgraded to 0.116
* Thu Jan 10 2019 Dweep Advani <dadvani@vmware.com> 0.113-4
- Fix for CVE-2018-19788
* Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 0.113-3
- Added pre and postun requires for shadow tools
* Thu Oct 05 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.113-2
- Enable PAM and systemd.
* Wed Oct 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.113-1
- Upgrade to 0.113-1
* Fri May 22 2015 Alexey Makhalov <amakhalov@vmware.com> 0.112-1
- initial version
