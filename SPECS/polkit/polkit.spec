Summary:           A toolkit for defining and handling authorizations.
Name:              polkit
Version:           121
Release:           4%{?dist}
Group:             Applications/System
Vendor:            VMware, Inc.
URL:               https://www.freedesktop.org/software/polkit/docs/latest/polkit.8.html
Distribution:      Photon

Source0: https://www.freedesktop.org/software/polkit/releases/%{name}-%{version}.tar.gz
%define sha512 %{name}=f565027b80f32833c558900b612e089ab25027da5bf9a90c421a292467d4db9a291f6dc9850c4bca8f9ee890d476fd064a643a5f7e28497661ba1e31d4227624
Source1:           %{name}.sysusers

Source2: license.txt
%include %{SOURCE2}

BuildRequires:     autoconf
BuildRequires:     meson
BuildRequires:     expat-devel
BuildRequires:     glib-devel
BuildRequires:     intltool >= 0.40.0
BuildRequires:     Linux-PAM-devel
BuildRequires:     systemd-devel
BuildRequires:     duktape-devel
BuildRequires:     gobject-introspection-devel

Requires:          duktape
Requires:          expat
Requires:          glib
Requires:          Linux-PAM
Requires:          systemd
Requires(pre):     systemd-rpm-macros
Requires(pre):     /usr/sbin/useradd /usr/sbin/groupadd

%description
polkit provides an authorization API intended to be used by privileged programs
(“MECHANISMS”) offering service to unprivileged programs (“SUBJECTS”) often
through some form of inter-process communication mechanism

%package           devel
Summary:           polkit development headers and libraries
Group:             Development/Libraries
Requires:          polkit = %{version}-%{release}

%description       devel
header files and libraries for polkit

%prep
%autosetup -p1 -n %{name}-v.%{version}

%build
%meson \
    -D js_engine=duktape \
  -D os_type=redhat \
  -D authfw=pam \
  -D examples=false \
  -D introspection=true \
  -D session_tracking=libsystemd-login \
  -D tests=false

%meson_build

%install
%meson_install
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
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%pre
%sysusers_create_compat %{SOURCE1}

%post
/sbin/ldconfig
# The implied (systemctl preset) will fail and complain, but the macro hides
# and ignores the fact.  This is in fact what we want, polkit.service does not
# have an [Install] section and it is always started on demand.
%systemd_post polkit.service

%preun
%systemd_preun polkit.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart polkit.service

%files
%defattr(-,root,root)
%{_bindir}/pk*
%{_libdir}/lib%{name}-*.so.*
%{_libdir}/polkit-1/polkit-agent-helper-1
%{_libdir}/polkit-1/polkitd
%{_unitdir}/polkit.service
%{_datadir}/dbus-1/system-services/org.freedesktop.PolicyKit1.service
%{_datadir}/locale/*
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%{_sysconfdir}/pam.d/polkit-1
%{_sysconfdir}/polkit-1/rules.d/50-default.rules
%{_datadir}/gettext/its
%{_libdir}/girepository-1.0/*.typelib
%{_datadir}/polkit-1/policyconfig-1.dtd
%{_sysusersdir}/%{name}.sysusers

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}-1/
%{_libdir}/lib%{name}-*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 121-4
- Release bump for SRP compliance
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 121-3
- Use systemd-rpm-macros for user creation
* Tue Jan 17 2023 Piyush Gupta <gpiyush@vmware.com> 121-2
- Set polkit uid to 1027 since it's not in range UID_MIN(1000) to UID_MAX(60000).
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 121-1
- Upgrade to v121
* Tue Oct 19 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.120-1
- Bump version as a part of mozjs upgrade
* Wed Apr 28 2021 Gerrit Photon <photon-checkins@vmware.com> 0.118-2
- Bump up release version since mozjs is update to 78.10.0
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
