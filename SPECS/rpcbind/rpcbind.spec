Summary:        RPC program number mapper
Name:           rpcbind
Version:        0.2.3
Release:        8%{?dist}
License:        BSD
URL:            http://nfsv4.bullopensource.org
Group:          Applications/Daemons
Source0:        http://downloads.sourceforge.net/rpcbind/%{name}-%{version}.tar.bz2
%define sha1 rpcbind=e79974a99d09b6d6fff9d86bf00225dc33723ce2
Source1:        rpcbind.service
Source2:        rpcbind.socket
Source3:        rpcbind.sysconfig
Patch0:         http://www.linuxfromscratch.org/patches/blfs/svn/rpcbind-0.2.3-tirpc_fix-1.patch
Patch1:         rpcbind-CVE-2017-8779.patch
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  libtirpc-devel
BuildRequires:  systemd
Requires:       libtirpc
Requires:       systemd
Requires(pre):  shadow
Requires(preun):shadow
Requires(post): coreutils

%description
The rpcbind program is a replacement for portmap. It is required for import or export of Network File System (NFS) shared directories. The rpcbind utility is a server that converts RPC program numbers into universal addresses

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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

%pre
rpcid=`getent passwd rpc | cut -d: -f 3`
if [ -n "$rpcid" -a "$rpcid" != "31" ]; then
	userdel  rpc 2> /dev/null || :
	groupdel rpc 2> /dev/null || :
fi
if [ -z "$rpcid" -o "$rpcid" != "31" ]; then
	groupadd -g 31 rpc > /dev/null 2>&1
	useradd -d /var/lib/rpcbind -g rpc -s /bin/false -u 31 rpc > /dev/null 2>&1
fi
%preun
%systemd_preun rpcbind.service rpcbind.socket
if [ $1 -eq 0 ]; then
	userdel  rpc 2>/dev/null || :
	groupdel rpc 2>/dev/null || :
fi

%post
/sbin/ldconfig
if [ $1 -eq 1 ] ; then
    chown -v root:sys /var/lib/rpcbind
fi
%systemd_post rpcbind.socket rpcbind.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart rpcbind.service rpcbind.socket

%clean
rm -rf %{buildroot}/*

%changelog
*	Thu May 18 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.2.3-8
-	Fix CVE-2017-8779
*	Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.2.3-7
-	add shadow and coreutils to requires
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.2.3-6
-	GA - Bump release of all rpms
*	Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 0.2.3-5
-	Edit scriptlets.
*	Fri Feb 05 2016 Anish Swaminathan <anishs@vmware.com> 0.2.3-4
-	Add pre install scripts in the rpm
*	Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> 0.2.3-3
-	Edit scripts in the rpm
*   	Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  0.2.3-2
-   	Add systemd to Requires and BuildRequires.
*	Tue Dec 8 2015 Divya Thaluru <dthaluru@vmware.com> 0.2.3-1
-	Initial build.	First version
