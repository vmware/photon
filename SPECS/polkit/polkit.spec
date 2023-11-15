Summary:       A toolkit for defining and handling authorizations.
Name:          polkit
Version:       0.116
Release:       6%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
License:       LGPLv2+
URL:           https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html
Distribution:  Photon

Source0:       https://www.freedesktop.org/software/polkit/releases/%{name}-%{version}.tar.gz
%define sha512 %{name}=b66b01cc2bb4349de70147f41f161f0f6f41e7230b581dfb054058b48969ec57041ab05b51787c749ccfc36aa5f317952d7e7ba337b4f6f6c0a923ed5866c2d5

Patch0:        CVE-2021-3560.patch
Patch1:        CVE-2021-4034.patch
Patch2:        CVE-2021-4115.patch

BuildRequires: autoconf
BuildRequires: expat-devel
BuildRequires: glib-devel >= 2.58.3
BuildRequires: gobject-introspection
BuildRequires: intltool >= 0.40.0
BuildRequires: mozjs60-devel
BuildRequires: Linux-PAM-devel
BuildRequires: systemd-devel

Requires:      mozjs60
Requires:      expat
Requires:      glib >= 2.58.3
Requires:      js
Requires:      Linux-PAM
Requires:      systemd
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):  /usr/sbin/userdel /usr/sbin/groupdel

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
    --with-systemdsystemunitdir=%{_libdir}/systemd/system
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete
install -vdm 755 %{buildroot}/etc/pam.d
cat > %{buildroot}/etc/pam.d/polkit-1 << "EOF"
# Begin /etc/pam.d/polkit-1

auth     include        system-auth
account  include        system-account
password include        system-password
session  include        system-session

# End /etc/pam.d/polkit-1
EOF

%pre
getent group polkitd > /dev/null || groupadd -fg 27 polkitd &&
getent passwd polkitd > /dev/null || \
    useradd -c "PolicyKit Daemon Owner" -d /etc/polkit-1 -u 27 \
        -g polkitd -s /bin/false polkitd
exit 0

%post
/sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
    systemctl stop polkit
    if getent passwd polkitd >/dev/null; then
        userdel polkitd
    fi
    if getent group polkitd >/dev/null; then
        groupdel polkitd
    fi
fi

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
%{_datadir}/gettext/its

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}-1/
%{_libdir}/lib%{name}-*.a
%{_libdir}/lib%{name}-*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Nov 15 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 0.116-6
- Version bump due to glib change
* Wed Jul 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.116-5
- Fix mozjs60 dependency
* Mon Feb 07 2022 Siju Maliakkal <smaliakkal@vmware.com> 0.116-4
- Fix for CVE-2021-4115
* Thu Jan 20 2022 Siju Maliakkal <smaliakkal@vmware.com> 0.116-3
- Fix for CVE-2021-4034
* Wed May 26 2021 Siju Maliakkal <smaliakkal@vmware.com> 0.116-2
- Fix for CVE-2021-3560
* Sat Oct 26 2019 Ankit Jain <ankitja@vmware.com> 0.116-1
- Upgraded to 0.116
* Fri Oct 11 2019 Siju Maliakkal <smaliakkal@vmware.com> 0.113-6
- Fix for CVE-2018-1116
- Combined patch CVE-2018-19788,CVE-2018-116,CVE-2019-6133 to one
* Thu May 23 2019 Siju Maliakkal <smaliakkal@vmware.com> 0.113-5
- Fix for CVE-2019-6133
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
