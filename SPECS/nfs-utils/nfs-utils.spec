Summary:	NFS client utils
Name:		nfs-utils
Version:	1.3.2
Release:	2%{?dist}
License:	GPLv2+
URL:		http://sourceforge.net/projects/nfs
Group:		Applications/Nfs-utils-client
Source0:    http://downloads.sourceforge.net/nfs/%{name}-%{version}.tar.bz2
%define sha1 nfs-utils=138ad690992d4784c05024d814a2d49ee8ebf6be
Source1:    nfs-client.service
Source2:    nfs-client.target
Source3:    rpc-statd.service
Source4:    rpc-statd-notify.service
Source5:    nfs-utils.defaults
Vendor:		VMware, Inc.
Distribution:	Photon
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
install -m644 %{SOURCE1} %{buildroot}/lib/systemd/system/
install -m644 %{SOURCE2} %{buildroot}/lib/systemd/system/
install -m644 %{SOURCE3} %{buildroot}/lib/systemd/system/
install -m644 %{SOURCE4} %{buildroot}/lib/systemd/system/
install -m644 %{SOURCE5} %{buildroot}/etc/default/nfs-utils

%files
%defattr(-,root,root)
%{_libdir}/*
%{_datadir}/*
/sbin/*
%{_sbindir}/*
%{_sharedstatedir}/*
/etc/default/nfs-utils
/lib/systemd/system/*

%changelog
*	Tue Dec 8 2015 Divya Thaluru <dthaluru@vmware.com> 1.3.2-2
-	Adding systemd service files
*	Tue Jul 14 2015 Rongrong Qiu <rqiu@vmware.com> 1.3.2-1
-	Initial build.	First version
