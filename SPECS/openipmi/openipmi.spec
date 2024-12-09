Summary:        A shared library implementation of IPMI and the basic tools
Name:           openipmi
Version:        2.0.33
Release:        7%{?dist}
URL:            https://sourceforge.net/projects/openipmi
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://sourceforge.net/projects/openipmi/files/latest/download/OpenIPMI-%{version}.tar.gz
%define sha512 OpenIPMI=615fccd1ffd4af18584c1b0e54667ba2de60b6d42b44e7448f27808114180fa3b31b4834276bdf69c3df1e5210df871fd888deec8186377524838390fe41e641

Source1: openipmi-helper
Source2: ipmi.service

Source3: license.txt
%include %{SOURCE3}

BuildRequires: systemd-devel
BuildRequires: perl
BuildRequires: popt-devel
BuildRequires: ncurses-devel
BuildRequires: openssl-devel
BuildRequires: swig
BuildRequires: python3-devel

Requires: systemd

%description
This package contains a shared library implementation of IPMI and the
basic tools used with OpenIPMI.

%package        devel
Summary:        Development files for OpenIPMI
Group:          Utilities
Requires:       %{name} = %{version}-%{release}
Requires:       ncurses-devel

%description devel
Contains additional files need for a developer to create applications
and/or middleware that depends on libOpenIPMI

%package        perl
Summary:        Perl interface for OpenIPMI
Group:          Utilities
Requires:       %{name} = %{version}-%{release}
Requires:       perl >= 5

%description    perl
A Perl interface for OpenIPMI.

%package        python3
Summary:        Python interface for OpenIPMI
Group:          Utilities
Requires:       %{name} = %{version}-%{release}
Requires:       python3

%description    python3
A Python interface for OpenIPMI.

%package        ui
Summary:        User Interface (ui)
Group:          Utilities
Requires:       %{name} = %{version}-%{release}

%description    ui
This package contains a user interface

%package        lanserv
Summary:        Emulates an IPMI network listener
Group:          Utilities
Requires:       %{name} = %{version}-%{release}

%description    lanserv
This package contains a network IPMI listener.

%prep
%autosetup -p1 -n OpenIPMI-%{version}

%build
# USERFIX: Things you might have to add to configure:
#  --with-tclcflags='-I /usr/include/tclN.M' --with-tcllibs=-ltclN.M
#    Obviously, replace N.M with the version of tcl on your system.
%configure                                  \
    --with-tcl=no                           \
    --disable-static                        \
    --with-tkinter=no                       \
    --docdir=%{_docdir}/%{name}-%{version}  \
    --with-perl=yes                         \
    --with-perlinstall=%{perl_vendorarch}   \
    --with-python=%{python3} \
    --with-pythoninstall=%{python3_sitelib}

%make_build

%install
# make doesn't support _smp_mflags
make DESTDIR=%{buildroot} install
install -d %{buildroot}%{_sysconfdir}/init.d
install -d %{buildroot}%{_sysconfdir}/sysconfig
install ipmi.init %{buildroot}%{_sysconfdir}/init.d/ipmi
install ipmi.sysconf %{buildroot}%{_sysconfdir}/sysconfig/ipmi

mkdir -p %{buildroot}%{_unitdir} \
         %{buildroot}/%{_libexecdir}

cp %{SOURCE1} %{buildroot}%{_libexecdir}/.
cp %{SOURCE2} %{buildroot}%{_unitdir}/ipmi.service

chmod 755 %{buildroot}%{_libexecdir}/openipmi-helper
install -vdm755 %{buildroot}%{_presetdir}
echo "disable ipmi.service" > %{buildroot}%{_presetdir}/50-ipmi.preset

%preun
%systemd_preun ipmi.service

%post
/sbin/ldconfig
%systemd_post ipmi.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart ipmi.service

%files
%defattr(-,root,root)
%{_libdir}/libOpenIPMI*.so.*
%exclude %{_sysconfdir}/init.d/ipmi
%config(noreplace) %{_sysconfdir}/sysconfig/ipmi
%{_libexecdir}/*
%{_unitdir}/ipmi.service
%{_presetdir}/50-ipmi.preset

%files perl
%defattr(-,root,root)
%{perl_vendorarch}/*

%files python3
%defattr(-,root,root,-)
%{python3_sitearch}/*OpenIPMI*

%files devel
%defattr(-,root,root)
%{_includedir}/OpenIPMI
%{_libdir}/*.so
%{_libdir}/pkgconfig

%files ui
%defattr(-,root,root)
%{_bindir}/ipmi_ui
%{_bindir}/ipmicmd
%{_bindir}/openipmicmd
%{_bindir}/openipmi_eventd
%{_bindir}/ipmish
%{_bindir}/openipmish
%{_bindir}/solterm
%{_bindir}/rmcp_ping
%{_libdir}/libOpenIPMIui.so.*
%{_mandir}/man1/ipmi_ui.1*
%{_mandir}/man1/openipmicmd.1*
%{_mandir}/man1/openipmish.1*
%{_mandir}/man1/openipmigui.1*
%{_mandir}/man1/solterm.1*
%{_mandir}/man1/openipmi_eventd.1.gz
%{_mandir}/man1/rmcp_ping.1*
%{_mandir}/man7/ipmi_cmdlang.7*
%{_mandir}/man7/openipmi_conparms.7*

%files lanserv
%defattr(-,root,root)
%{_bindir}/ipmilan
%{_bindir}/ipmi_sim
%{_bindir}/sdrcomp
%{_libdir}/libIPMIlanserv.so.*
%config(noreplace) %{_sysconfdir}/ipmi/ipmisim1.emu
%config(noreplace) %{_sysconfdir}/ipmi/lan.conf
%{_mandir}/man8/ipmilan.8*
%{_mandir}/man1/ipmi_sim.1.gz
%{_mandir}/man5/ipmi_lan.5.gz
%{_mandir}/man5/ipmi_sim_cmd.5.gz

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.33-7
- Release bump for SRP compliance
* Thu Jun 01 2023 Nitesh Kumar <kunitesh@vmware.com> 2.0.33-6
- Bump version as a part of ncurses upgrade to v6.4
* Thu Jan 12 2023 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.0.33-5
- Bump up version no. as part of swig upgrade
* Thu Dec 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.0.33-4
- Bump version as a part of readline upgrade
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 2.0.33-3
- Perl versiion upgraded to 5.36.0
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.33-2
- Update release to compile with python 3.11
* Wed Sep 28 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.33-1
- Automatic Version Bump
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.32-1
- Automatic Version Bump
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.31-2
- Bump up release for openssl
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.0.31-1
- Automatic Version Bump
* Tue Oct 13 2020 Tapas Kundu <tkundu@vmware.com> 2.0.29-4
- Use python 3.9
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 2.0.29-3
- openssl 1.1.1
* Mon Jul 27 2020 Tapas Kundu <tkundu@vmware.com> 2.0.29-2
- Use python 3.8
* Mon Jun 22 2020 Tapas Kundu <tkundu@vmware.com> 2.0.29-1
- Build with python3
- Mass removal python2
* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 2.0.25-2
- Added BuildRequires python2-devel
* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.0.25-1
- Upgrade to 2.0.25
* Fri Sep 15 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.24-2
- openipmi-devel requires ncurses-devel
* Mon Sep 11 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.24-1
- Initial build.  First version
