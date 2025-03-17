Summary:        Fast incremental file transfer.
Name:           rsync
Version:        3.4.1
Release:        1%{?dist}
URL:            https://rsync.samba.org
Group:          Appication/Internet
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://download.samba.org/pub/rsync/src/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  zlib-devel
BuildRequires:  systemd
BuildRequires:  lz4-devel
BuildRequires:  systemd-devel
BuildRequires:  xxhash-devel
BuildRequires:  openssl-devel

Requires:       xxhash
Requires:       lz4
Requires:       zlib
Requires:       systemd

%description
Rsync is a fast and extraordinarily versatile file copying tool.
It can copy locally, to/from another host over any remote shell,
or to/from a remote rsync daemon.
It offers a large number of options that control every aspect of its
behavior and permit very flexible specification of the set of files
to be copied. It is famous for its delta-transfer algorithm, which
reduces the amount of data sent over the network by sending only the
differences between the source files and the existing files in the
destination.
Rsync is widely used for backups and mirroring and as an improved
copy command for everyday use.

%prep
%autosetup -p1

%build
%configure \
    --with-included-zlib=no \
    --enable-xxhash \
    --enable-zstd \
    --enable-lz4 \
    --enable-ipv6

%make_build

%install
%make_install %{?_smp_mflags}
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/rsyncd.conf

mkdir -p %{buildroot}%{_unitdir}
cat << EOF >> %{buildroot}%{_unitdir}/rsyncd.service
[Unit]
Description=Rsync Server
After=local-fs.target
ConditionPathExists=%{_sysconfdir}/rsyncd.conf

[Service]
ExecStart=%{_bindir}/%{name} --daemon --no-detach

[Install]
WantedBy=multi-user.target
EOF

%if 0%{?with_check}
%check
make %{?_smp_mflags} check
%endif

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_unitdir}/rsyncd.service
%{_sysconfdir}/rsyncd.conf
%exclude %dir %{_libdir}/debug

%changelog
* Fri Jan 17 2025 Tapas Kundu <tapas.kundu@broadcom.com> 3.4.1-1
- Update to 3.4.1
* Thu Jan 02 2025 Tapas Kundu <tapas.kundu@broadcom.com> 3.2.7-5
- Fixed CVE-2024-12084,CVE-2024-12085,CVE-2024-12086,CVE-2024-12087,
- CVE-2024-12088,CVE-2024-12747
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.2.7-4
- Release bump for SRP compliance
* Tue Dec 10 2024 Tapas Kundu <tapas.kundu@broadcom.com> 3.2.7-3
- Some checksum buffer fixes
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.2.7-2
- Bump version as a part of zlib upgrade
* Fri Oct 28 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2.7-1
- Automatic Version Bump
* Tue Oct 04 2022 Oliver Kurth <okurth@vmware.com> 3.2.6-1
- Update to 3.2.6
* Wed Aug 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.2.4-3
- Fix CVE-2022-29154
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.2.4-2
- Fix binary path
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2.4-1
- Automatic Version Bump
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.2.3-3
- Bump up release for openssl
* Fri Jun 11 2021 Ankit Jain <ankitja@vmware.com> 3.2.3-2
- Fix CVE-2020-14387
* Fri Aug 14 2020 Gerrit Photon <photon-checkins@vmware.com> 3.2.3-1
- Automatic Version Bump
* Thu Jul 09 2020 Gerrit Photon <photon-checkins@vmware.com> 3.2.2-1
- Automatic Version Bump
* Mon Oct 15 2018 Ankit Jain <ankitja@vmware.com> 3.1.3-2
- Building rsync with system zlib instead of outdated zlib in rsync source
* Tue May 01 2018 Xiaolin Li <xiaolinl@vmware.com> 3.1.3-1
- Updated to version 3.1.3, fix CVE-2018-5764
* Wed Dec 27 2017 Xiaolin Li <xiaolinl@vmware.com> 3.1.2-5
- Fix CVE-2017-17433, CVE-2017-17434
* Wed Nov 29 2017 Xiaolin Li <xiaolinl@vmware.com> 3.1.2-4
- Fix CVE-2017-16548
* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 3.1.2-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.2-2
- GA - Bump release of all rpms
* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 3.1.2-1
- Updated to version 3.1.2
* Mon Dec 14 2015 Xiaolin Li < xiaolinl@vmware.com> 3.1.1-1
- Initial build. First version
