Summary:        NFS client utils
Name:           nfs-utils
Version:        2.1.1
Release:        2%{?dist}
License:        GPLv2+
URL:            http://sourceforge.net/projects/nfs
Group:          Applications/Nfs-utils-client
Source0:        http://downloads.sourceforge.net/nfs/%{name}-%{version}.tar.bz2
%define sha1    nfs-utils=8f86ffef3bfc954f3ef9aee805b35cdca3802b14
Source1:        nfs-client.service
Source2:        nfs-client.target
Source3:        rpc-statd.service
Source4:        rpc-statd-notify.service
Source5:        nfs-utils.defaults
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  krb5
BuildRequires:  libtirpc-devel
BuildRequires:  python3-devel
Requires:       libtirpc
Requires:       rpcbind
Requires:       shadow
Requires:       python3-libs

%description
The nfs-utils package contains simple nfs client service

%prep
%setup -q -n %{name}-%{version}
#not prevent statd to start
sed -i "/daemon_init/s:\!::" utils/statd/statd.c
find . -iname "*.py" | xargs -I file sed -i '1s/python/python3/g' file

%build
./configure --prefix=%{_prefix}          \
            --sysconfdir=%{_sysconfdir}      \
            --enable-libmount-mount \
            --without-tcp-wrappers \
            --disable-nfsv4        \
            --disable-gss \
            --disable-static

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
*   Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.1.1-2
-   Build with python3.
*   Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.1-1
-   Update to 2.1.1
*   Fri Dec 16 2016 Nick Shi <nshi@vmware.com> 1.3.3-6
-   Requires rpcbind.socket upon starting rpc-statd service (bug 1668405)
*   Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.3.3-5
-   add shadow to requires
*   Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 1.3.3-4
-   Removed packaging of debug files
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
