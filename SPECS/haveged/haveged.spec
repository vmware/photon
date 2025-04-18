Summary:        A Linux entropy source using the HAVEGE algorithm
Name:           haveged
Version:        1.9.18
Release:        3%{?dist}
License:        GPLv3+
Vendor:         VMware, Inc.
Distribution:   Photon
Group:          System Environment/Daemons
URL:            http://www.irisa.fr/caps/projects/hipsor

Source0: http://www.issihosts.com/haveged/%{name}-%{version}.tar.gz
%define sha512 %{name}=ef2e0ae3be68a8fba16371c3347d52ecf9748269ae30eef2e5c26aad6cfb516f87295e1e56be902df1064e7d4ace04863dd094d62b69e584608f779d63b42d8e

Source1:        %{name}.service

Requires:       systemd

BuildRequires:  systemd-devel
BuildRequires:  automake
BuildRequires:  coreutils >= 9.1-7
BuildRequires:  glibc

%description
A Linux entropy source using the HAVEGE algorithm

Haveged is a user space entropy daemon which is not dependent upon the
standard mechanisms for harvesting randomness for the system entropy
pool. This is important in systems with high entropy needs or limited
user interaction (e.g. headless servers).

Haveged uses HAVEGE (HArdware Volatile Entropy Gathering and Expansion)
to maintain a 1M pool of random bytes used to fill /dev/random
whenever the supply of random bits in /dev/random falls below the low
water mark of the device. The principle inputs to haveged are the
sizes of the processor instruction and data caches used to setup the
HAVEGE collector. The haveged default is a 4kb data cache and a 16kb
instruction cache. On machines with a cpuid instruction, haveged will
attempt to select appropriate values from internal tables.

%package        devel
Summary:        Headers and shared development libraries for HAVEGE algorithm
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
Headers and shared object symbolic links for the HAVEGE algorithm

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

rm -rf %{buildroot}%{_sysconfdir}/init.d \
       %{buildroot}%{_libdir}/libhavege.*a

mkdir -p %{buildroot}%{_unitdir}
install -p -m644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%if 0%{?with_check}
%check
make check %{?_smp_mflags}
%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%files
%defattr(-, root, root, -)
%{_sbindir}/%{name}
%{_unitdir}/%{name}.service
%{_libdir}/*so.*

%files devel
%defattr(-, root, root, -)
%{_mandir}/man8/%{name}.8*
%{_mandir}/man3/libhavege.3*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/havege.h
%{_libdir}/*.so

%changelog
* Wed Oct 16 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.9.18-3
- Require coreutils only
* Sun Feb 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.9.18-2
- Fix build requires
* Sun May 29 2022 Gerrit Photon <photon-checkins@vmware.com> 1.9.18-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.9.14-1
- Automatic Version Bump
* Thu Jul 16 2020 Gerrit Photon <photon-checkins@vmware.com> 1.9.13-1
- Automatic Version Bump
* Thu May 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.9.1-4
- Start haveged before cloud-init-local.service to speed up booting.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.1-3
- GA - Bump release of all rpms
* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 1.9.1-2
- Add systemd requirement.
* Sun Jan 13 2013 Jirka Hladky <hladky.jiri@gmail.com> - 1.7h-0
- Couple of minor updates
* Sat Jan 12 2013 Jirka Hladky <hladky.jiri@gmail.com> - 1.7g-0
- Updated to the version 1.7
- Version 1.7 brings developement libraries
- Added devel package
* Sat Oct 13 2012 Jirka Hladky <hladky.jiri@gmail.com> - 1.5-2
- BZ 850144
- Introduce new systemd-rpm macros in haveged spec file
- Fedora 19 changes the way how to work with services in spec files.
- It introduces new macros - systemd_post, systemd_preun and systemd_postun;
- which replace scriptlets from Fedora 18 and older
- see https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Systemd
* Tue Aug 14 2012 Jirka Hladky <hladky.jiri@gmail.com> - 1.5-1
- Update to the version 1.5
- Main new feature is a run time verification of the produced random numbers
- PIDFILE set to /run/haveged.pid
- converted README and man page to UTF-8. Informed the upstream to fix it.
* Wed Feb 15 2012 Jirka Hladky <hladky.jiri@gmail.com> - 1.4-3
- PIDFile should be stored at /run instead of the default location /var/run
- There is  long term plan that directory /var/run will not further exist in the future Fedora versions
- Asked upstream to add -p <PID_FILE_location> switch to influence the location of the PID File
- Set PIDFile=/var/run/haveged.pid This is needed as long -p option is not implemented
- https://bugzilla.redhat.com/show_bug.cgi?id=770306#c10
* Wed Feb 15 2012 Jirka Hladky <hladky.jiri@gmail.com> - 1.4-2
- Updated systemd service file, https://bugzilla.redhat.com/show_bug.cgi?id=770306
* Tue Feb 14 2012 Jirka Hladky <hladky.jiri@gmail.com> - 1.4-1
- Update to the version 1.4
- Conversion to systemd, drop init script
* Sun Nov 06 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.3-2
- Fixed a bug on non x86 systems
* Sat Nov 05 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.3-1
- update from the upstream (1.3 stable)
* Mon Oct 03 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.3-0
-version 1.3 beta
* Fri Sep 30 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2-4
- ppc64 build
* Mon Sep 26 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2-3
- Cleaned spec file according to https://bugzilla.redhat.com/show_bug.cgi?id=739347#c11
* Sat Sep 24 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2-2
- Added comment to explain why we need use Fedora specific start script
* Wed Sep 21 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2-1
- Cleaned spec file according to https://bugzilla.redhat.com/show_bug.cgi?id=739347#c1
* Wed Sep 07 2011  Jirka Hladky <hladky.jiri@gmail.com> - 1.2-0
- Initial build
