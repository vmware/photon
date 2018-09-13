Summary:        A shared library implementation of IPMI and the basic tools
Name:           openipmi
Version:        2.0.25
Release:        1%{?dist}
URL:            https://sourceforge.net/projects/openipmi/
License:        LGPLv2+ and GPLv2+ or BSD
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://sourceforge.net/projects/openipmi/files/latest/download/%{name}-%{version}.tar.gz
%define sha1    openipmi=06751d0cd4353edc9711405f829fa7039533239d
Source1:        openipmi-helper
Source2:        ipmi.service
BuildRequires:  systemd
BuildRequires:  perl
BuildRequires:  popt-devel
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  swig
Requires:       systemd

%description
This package contains a shared library implementation of IPMI and the
basic tools used with OpenIPMI.

%package        devel
Summary:        Development files for OpenIPMI
Group:          Utilities
Requires:       openipmi = %{version}
Requires:       ncurses-devel

%description devel
Contains additional files need for a developer to create applications
and/or middleware that depends on libOpenIPMI

%package        perl
Summary:        Perl interface for OpenIPMI
Group:          Utilities
Requires:       openipmi = %{version}-%{release}, perl >= 5

%description    perl
A Perl interface for OpenIPMI.

%package        python
Summary:        Python interface for OpenIPMI
Group:          Utilities
Requires:       openipmi = %{version}-%{release}, python2

%description    python
A Python interface for OpenIPMI.

%package        ui
Summary:        User Interface (ui)
Group:          Utilities
Requires:       openipmi = %{version}-%{release}

%description    ui
This package contains a user interface

%package        lanserv
Summary:        Emulates an IPMI network listener
Group:          Utilities
Requires:       openipmi = %{version}-%{release}

%description    lanserv
This package contains a network IPMI listener.

%prep
%setup -n OpenIPMI-%{version}

%build
# USERFIX: Things you might have to add to configure:
#  --with-tclcflags='-I /usr/include/tclN.M' --with-tcllibs=-ltclN.M
#    Obviously, replace N.M with the version of tcl on your system.
./configure                                 \
    --prefix=/usr                           \
    --with-tcl=no                           \
    --disable-static                        \
    --with-tkinter=no                       \
    --docdir=%{_docdir}/%{name}-%{version}  \
    --with-perl=yes                         \
    --with-perlinstall=%{perl_vendorarch}   \
    --sysconfdir=%{_sysconfdir}
make

%install
make DESTDIR=%{buildroot} install
install -d %{buildroot}/etc/init.d
install -d %{buildroot}/etc/sysconfig
install ipmi.init %{buildroot}/etc/init.d/ipmi
install ipmi.sysconf %{buildroot}/etc/sysconfig/ipmi
find %{buildroot}/%{_libdir} -name '*.la' -delete
mkdir -p %{buildroot}/lib/systemd/system
mkdir -p %{buildroot}/%{_libexecdir}
cp %{SOURCE1} %{buildroot}/%{_libexecdir}/.
cp %{SOURCE2} %{buildroot}/lib/systemd/system/ipmi.service
chmod 755 %{buildroot}/%{_libexecdir}/openipmi-helper
install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable ipmi.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-ipmi.preset

#The build VM does not support ipmi.
#%check
#make %{?_smp_mflags} check

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
%{_libdir}/libOpenIPMIcmdlang.so.*
%{_libdir}/libOpenIPMIposix.so.*
%{_libdir}/libOpenIPMIpthread.so.*
%{_libdir}/libOpenIPMI.so.*
%{_libdir}/libOpenIPMIutils.so.*
%doc COPYING COPYING.LIB FAQ INSTALL README README.Force
%doc README.MotorolaMXP CONFIGURING_FOR_LAN COPYING.BSD
%exclude /etc/init.d/ipmi
%config(noreplace) %{_sysconfdir}/sysconfig/ipmi
%{_libexecdir}/*
/lib/systemd/system/ipmi.service
%{_libdir}/systemd/system-preset/50-ipmi.preset

%files perl
%defattr(-,root,root)
%{perl_vendorarch}
%doc swig/OpenIPMI.i swig/perl/sample swig/perl/ipmi_powerctl

%files python
%defattr(-,root,root)
%{_libdir}/python*/site-packages/*OpenIPMI.*
%doc swig/OpenIPMI.i

%files devel
%defattr(-,root,root)
%{_includedir}/OpenIPMI
%{_libdir}/*.so
%{_libdir}/pkgconfig
%doc doc/IPMI.pdf

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
*   Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.0.25-1
-   Upgrade to 2.0.25
*   Fri Sep 15 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.24-2
-   openipmi-devel requires ncurses-devel
*   Mon Sep 11 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.24-1
-   Initial build.  First version

