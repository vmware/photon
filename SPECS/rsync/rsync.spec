Summary:	Fast incremental file transfer. 
Name:		rsync
Version:	3.1.2
Release:	3%{?dist}
License:	GPLv3+
URL:		https://rsync.samba.org/
Source0:	https://download.samba.org/pub/rsync/src/%{name}-%{version}.tar.gz
%define sha1 rsync=0d4c7fb7fe3fc80eeff922a7c1d81df11dbb8a1a
Group:		Appication/Internet
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	systemd
Requires:	systemd
%description
Rsync is a fast and extraordinarily versatile file copying tool. It can copy locally, to/from another host over any remote shell, or to/from a remote rsync daemon. It offers a large number of options that control every aspect of its behavior and permit very flexible specification of the set of files to be copied. It is famous for its delta-transfer algorithm, which reduces the amount of data sent over the network by sending only the differences between the source files and the existing files in the destination. Rsync is widely used for backups and mirroring and as an improved copy command for everyday use.
%prep
%setup -q
%build
%configure --prefix=/usr
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/%{_sysconfdir} 
touch %{buildroot}/%{_sysconfdir}/rsyncd.conf

mkdir -p %{buildroot}/%{_libdir}/systemd/system
cat << EOF >> %{buildroot}/%{_libdir}/systemd/system/rsyncd.service
[Unit]
Description=Rsync Server
After=local-fs.target
ConditionPathExists=/etc/rsyncd.conf

[Service]
ExecStart=/usr/bin/rsync --daemon --no-detach

[Install]
WantedBy=multi-user.target
EOF

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%exclude %{_libdir}/debug
%exclude /usr/src/debug
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_libdir}/systemd/system/rsyncd.service
%{_sysconfdir}/rsyncd.conf
%changelog
*       Wed Oct 05 2016 ChangLee <changlee@vmware.com> 3.1.2-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.2-2
-	GA - Bump release of all rpms
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 3.1.2-1
-   Updated to version 3.1.2
*	Mon Dec 14 2015 Xiaolin Li < xiaolinl@vmware.com> 3.1.1-1
-	Initial build. First version

