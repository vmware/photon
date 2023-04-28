Summary:          NFS client utils
Name:             nfs-utils
Version:          2.6.2
Release:          5%{?dist}
License:          GPLv2+
URL:              http://sourceforge.net/projects/nfs
Group:            Applications/Nfs-utils-client
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: https://sourceforge.net/projects/nfs/files/nfs-utils/%{version}/%{name}-%{version}.tar.xz
%define sha512 %{name}=60ef0dc1842fe751c142313d41e3494a0d2bd8db4b859e970456b711688a606938273f3b43fe66ba9725e0b4e7dc7301e7358504b2f1d2da60cbd3b9f171c103

Source1:          nfs-client.service
Source2:          nfs-client.target
Source3:          rpc-statd.service
Source4:          rpc-statd-notify.service
Source5:          %{name}.defaults
Source6:          nfs-server.service
Source7:          nfs-mountd.service
Source8:          %{name}.sysusers

BuildRequires:    libtool
BuildRequires:    krb5-devel
BuildRequires:    libcap-devel
BuildRequires:    libtirpc-devel
BuildRequires:    python3-devel
BuildRequires:    libevent-devel
BuildRequires:    device-mapper-devel
BuildRequires:    systemd-devel
BuildRequires:    keyutils-devel
BuildRequires:    sqlite-devel
BuildRequires:    libgssglue-devel
BuildRequires:    libnfsidmap-devel
BuildRequires:    e2fsprogs-devel
BuildRequires:    rpcsvc-proto-devel

Requires:         libtirpc
Requires:         rpcbind
Requires:         shadow
Requires:         python3-libs
Requires(pre):    systemd-rpm-macros
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd

%description
The %{name} package contains simple nfs client service.

%package devel
Summary: Development libraries and headers for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
Development libraries and headers for %{name}

%prep
%autosetup -p1 -n %{name}-%{version}
#not prevent statd to start
sed -i "/daemon_init/s:\!::" utils/statd/statd.c
sed '/unistd.h/a#include <stdint.h>' -i support/nsm/rpc.c
# fix --with-rpcgen=internal
sed -i 's/RPCGEN_PATH" =/rpcgen_path" =/' configure

%build
%configure \
   --enable-libmount-mount \
   --without-tcp-wrappers \
   --enable-gss \
   --enable-nfsv4 \
   --disable-static
# fix building against new gcc
sed -i 's/CFLAGS = -g/CFLAGS = -Wno-error=strict-prototypes/' support/nsm/Makefile
%make_build

%install
%make_install %{?_smp_mflags}
install -v -m644 utils/mount/nfsmount.conf %{_sysconfdir}/nfsmount.conf

mkdir -p %{buildroot}%{_unitdir} \
         %{buildroot}%{_sysconfdir}/default \
         %{buildroot}%{_sysconfdir}/export.d \
         %{buildroot}%{_sharedstatedir}/nfs/v4recovery

touch %{buildroot}%{_sysconfdir}/exports
install -m644 %{SOURCE1} %{buildroot}%{_unitdir}
install -m644 %{SOURCE2} %{buildroot}%{_unitdir}
install -m644 %{SOURCE3} %{buildroot}%{_unitdir}
install -m644 %{SOURCE4} %{buildroot}%{_unitdir}
install -m644 %{SOURCE5} %{buildroot}%{_sysconfdir}/default/%{name}
install -m644 %{SOURCE6} %{buildroot}%{_unitdir}
install -m644 %{SOURCE7} %{buildroot}%{_unitdir}
install -m644 systemd/proc-fs-nfsd.mount %{buildroot}%{_unitdir}
install -m644 systemd/nfs-idmapd.service %{buildroot}%{_unitdir}
install -m644 systemd/rpc_pipefs.target  %{buildroot}%{_unitdir}
install -m644 systemd/var-lib-nfs-rpc_pipefs.mount  %{buildroot}%{_unitdir}
install -m644 systemd/rpc-svcgssd.service %{buildroot}%{_unitdir}
install -p -D -m 0644 %{SOURCE8} %{buildroot}%{_sysusersdir}/%{name}.sysusers
install -vdm755 %{buildroot}%{_presetdir}
echo "disable nfs-server.service" > %{buildroot}%{_presetdir}/50-nfs-server.preset

mv %{buildroot}/sbin/* %{buildroot}%{_sbindir}

%if 0%{?with_check}
%check
#ignore test that might require additional setup
sed -i '/check_root/i \
exit 77' tests/t0001-statd-basic-mon-unmon.sh
make check %{?_smp_mflags}
%endif

%pre
%sysusers_create_compat %{SOURCE8}

%post
/sbin/ldconfig
%systemd_post nfs-server.service

%preun
%systemd_preun nfs-server.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart nfs-server.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/default/%{name}
%config(noreplace) %{_sysconfdir}/exports
%{_sbindir}/*
%{_sharedstatedir}/*
%{_unitdir}/*
%{_libdir}/libnfsidmap.so.*
%{_libexecdir}/nfsrahead
%{_presetdir}/50-nfs-server.preset
%{_udevrulesdir}/99-nfs.rules
%attr(0600,root,root) %config(noreplace) %{_libdir}/modprobe.d/50-nfs.conf
%{_sysusersdir}/%{name}.sysusers

%files devel
%defattr(-,root,root)
%{_datadir}/*
%{_includedir}/*
%{_libdir}/libnfsidmap.so
%{_libdir}/libnfsidmap/*.so
%{_libdir}/pkgconfig/libnfsidmap.pc

%changelog
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 2.6.2-5
- Use systemd-rpm-macros for user creation
* Thu Jan 26 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.6.2-4
- Bump version as a part of krb5 upgrade
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 2.6.2-3
- bump release as part of sqlite update
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.6.2-2
- Bump version as a part of libtirpc upgrade
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.6.2-1
- Upgrade to v2.6.2
* Sat Jul 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.6.1-3
- Bump version as a part of sqlite upgrade
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.6.1-2
- Fix binary path
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.6.1-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 2.5.3-1
- Automatic Version Bump
* Sun Nov 22 2020 Tapas Kundu <tkundu@vmware.com> 2.5.1-2
- Restrict nfs-mountd to start after rpcbind.socket
* Thu Jul 16 2020 Tapas Kundu <tkundu@vmware.com> 2.5.1-1
- Automatic Version Bump
- Use system installed rpcgen
* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 2.3.3-2
- Fix compilation issue against glibc-2.28
- Use internal rpcgen, deactivate librpcsecgss dependency.
* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.3.3-1
- Update to 2.3.3
* Thu Jun 07 2018 Anish Swaminathan <anishs@vmware.com> 2.3.1-2
- Add noreplace qualifier to config files
* Fri Jan 26 2018 Xiaolin Li <xiaolinl@vmware.com> 2.3.1-1
- Update to 2.3.1 and enable nfsv4
* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> 2.1.1-7
- No direct toybox dependency, shadow depends on toybox
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 2.1.1-6
- Requires shadow or toybox
* Thu Aug 24 2017 Alexey Makhalov <amakhalov@vmware.com> 2.1.1-5
- Fix compilation issue for glibc-2.26
* Wed Aug 16 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.1-4
- Add check and ignore test that fails.
* Tue Aug 8 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.1-3
- Alter nfs-server and nfs-mountd service files to use
- environment file and port opts.
* Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.1-2
- Build with python3.
* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.1-1
- Update to 2.1.1
* Fri Dec 16 2016 Nick Shi <nshi@vmware.com> 1.3.3-6
- Requires rpcbind.socket upon starting rpc-statd service (bug 1668405)
* Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.3.3-5
- add shadow to requires
* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 1.3.3-4
- Removed packaging of debug files
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.3.3-3
- GA - Bump release of all rpms
* Thu Apr 28 2016 Xiaolin Li <xiaolinl@vmware.com> 1.3.3-2
- Add nfs-server.service to rpm.
* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 1.3.3-1
- Updated to version 1.3.3
* Tue Dec 8 2015 Divya Thaluru <dthaluru@vmware.com> 1.3.2-2
- Adding systemd service files
* Tue Jul 14 2015 Rongrong Qiu <rqiu@vmware.com> 1.3.2-1
- Initial build. First version
