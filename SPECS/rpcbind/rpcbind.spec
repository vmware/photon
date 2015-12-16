Summary:	RPC program number mapper
Name:		rpcbind
Version:	0.2.3
Release:	2%{?dist}
License:	BSD
URL:		http://nfsv4.bullopensource.org
Group:	    Applications/Daemons
Source0:    http://downloads.sourceforge.net/rpcbind/%{name}-%{version}.tar.bz2
%define sha1 rpcbind=e79974a99d09b6d6fff9d86bf00225dc33723ce2
Source1:    rpcbind.service
Source2:    rpcbind.socket
Source3:    rpcbind.sysconfig
Patch0:     http://www.linuxfromscratch.org/patches/blfs/svn/rpcbind-0.2.3-tirpc_fix-1.patch
Vendor:     VMware, Inc.
Distribution:   Photon
BuildRequires:	libtirpc-devel
BuildRequires:  systemd
Requires:       libtirpc
Requires:       systemd
%description
The rpcbind program is a replacement for portmap. It is required for import or export of Network File System (NFS) shared directories. The rpcbind utility is a server that converts RPC program numbers into universal addresses
%prep
%setup -q
%patch0 -p1
%build
sed -i "/servname/s:rpcbind:sunrpc:" src/rpcbind.c
./configure --prefix=%{_prefix}      \
            --bindir=%{_sbindir}     \
            --enable-warmstarts \
            --disable-debug \
            --with-statedir=%{_localstatedir}/lib/rpcbind \
            --with-rpcuser=rpc
make
%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_localstatedir}/lib/rpcbind
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/sysconfig
install -m644 %{SOURCE1} %{buildroot}%{_unitdir}
install -m644 %{SOURCE2} %{buildroot}%{_unitdir}
install -m644 %{SOURCE3} %{buildroot}/etc/sysconfig/rpcbind

%files
%defattr(-,root,root)
%config(noreplace) /etc/sysconfig/rpcbind
%{_sbindir}/*
%{_mandir}/man8/*
%dir %{_localstatedir}/lib/rpcbind
%{_unitdir}/*

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%preun
systemctl disable rpcbind.socket >/dev/null 2>&1
systemctl disable rpcbind.service >/dev/null 2>&1

%post
/sbin/ldconfig
chown -v root:sys /var/lib/rpcbind
if ! getent group rpc >/dev/null; then
	groupadd -g 31 rpc
fi
if ! getent passwd rpc >/dev/null; then
	useradd -d /var/lib/rpcbind -g rpc -s /bin/false -u 31 rpc
fi
systemctl enable rpcbind.socket >/dev/null 2>&1
systemctl enable rpcbind.service >/dev/null 2>&1


%postun
/sbin/ldconfig
if getent passwd rpc >/dev/null; then
	userdel rpc
fi
if getent group rpc >/dev/null; then
	groupdel rpc
fi
systemctl disable rpcbind.socket >/dev/null 2>&1
systemctl disable rpcbind.service >/dev/null 2>&1
%clean
rm -rf %{buildroot}/*
%changelog
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  0.2.3-2
-   Add systemd to Requires and BuildRequires.
*	Tue Dec 8 2015 Divya Thaluru <dthaluru@vmware.com> 0.2.3-1
-	Initial build.	First version
