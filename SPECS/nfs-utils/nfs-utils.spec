Summary:    NFS client utils
Name:       nfs-utils
Version:    1.3.3
Release:    5%{?dist}
License:    GPLv2+
URL:        http://sourceforge.net/projects/nfs
Group:      Applications/Nfs-utils-client
Source0:    http://downloads.sourceforge.net/nfs/%{name}-%{version}.tar.bz2
%define sha1 nfs-utils=7c561e6a22a626aed93766bdb0c34e9a4e77b9e7
Source1:    nfs-client.service
Source2:    nfs-client.target
Source3:    rpc-statd.service
Source4:    rpc-statd-notify.service
Source5:    nfs-utils.defaults
Vendor:     VMware, Inc.
Distribution:   Photon
BuildRequires:  krb5
BuildRequires:  libtirpc-devel
Requires:   python2-libs
Requires:   libtirpc
Requires:   rpcbind

%description
The nfs-utils package contains simple nfs client service

%prep
%setup -q -n %{name}-%{version}
#not prevent statd to start
sed -i "/daemon_init/s:\!::" utils/statd/statd.c
%build
./configure --prefix=%{_prefix}          \
            --sysconfdir=%{_sysconfdir}      \
            --enable-libmount-mount \
            --without-tcp-wrappers \
            --disable-nfsv4        \
            --disable-gss
make
%install
make DESTDIR=%{buildroot} install
install -v -m644 utils/mount/nfsmount.conf /etc/nfsmount.conf

mkdir -p %{buildroot}/lib/systemd/system/
mkdir -p %{buildroot}/etc/default
mkdir -p %{buildroot}/etc/export.d
mkdir -p %{buildroot}/var/lib/nfs/v4recovery
touch %{buildroot}/etc/exports

install -m644 %{SOURCE1} %{buildroot}/lib/systemd/system/
install -m644 %{SOURCE2} %{buildroot}/lib/systemd/system/
install -m644 %{SOURCE3} %{buildroot}/lib/systemd/system/
install -m644 %{SOURCE4} %{buildroot}/lib/systemd/system/
install -m644 %{SOURCE5} %{buildroot}/etc/default/nfs-utils
install -m644 systemd/nfs-server.service %{buildroot}/lib/systemd/system/
install -m644 systemd/proc-fs-nfsd.mount %{buildroot}/lib/systemd/system/
install -m644 systemd/nfs-mountd.service %{buildroot}/lib/systemd/system/

%files
%defattr(-,root,root)
%{_datadir}/*
/sbin/*
%{_sbindir}/*
%{_sharedstatedir}/*
/etc/default/nfs-utils
/etc/exports
/lib/systemd/system/*

%changelog
*   Fri Jun 23 2017 Divya Thaluru <dthaluru@vmware.com> 1.3.3-5
-   Removed packaging of debug files
*   Fri Jun 03 2016 Nick Shi <nshi@vmware.com> 1.3.3-4
-   Requires rpcbind.socket upon starting rpc-statd service (bug 1668405)
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.3.3-3
-   GA - Bump release of all rpms
*   Thu Apr 28 2016 Xiaolin Li <xiaolinl@vmware.com> 1.3.3-2
-   Add nfs-server.service to rpm.
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 1.3.3-1
-   Updated to version 1.3.3
*   Tue Dec 8 2015 Divya Thaluru <dthaluru@vmware.com> 1.3.2-2
-   Adding systemd service files
*   Tue Jul 14 2015 Rongrong Qiu <rqiu@vmware.com> 1.3.2-1
-   Initial build.  First version
