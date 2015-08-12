Summary:	NFS client utils
Name:		nfs-utils
Version:	1.3.2
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.linuxfromscratch.org/
Group:		Applications/Nfs-utils-client
Source0:	 http://downloads.sourceforge.net/nfs/%{name}-%{version}.tar.bz2
%define sha1 nfs-utils=138ad690992d4784c05024d814a2d49ee8ebf6be
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires: krb5
BuildRequires: libtirpc-devel
Requires: python2-libs
Requires: libtirpc

%description
The nfs-utils package contains simple nfs client service

%prep
%setup -q -n %{name}-%{version}
#not prevent statd to start
sed -i "/daemon_init/s:\!::" utils/statd/statd.c
%build
./configure --prefix=%{_prefix}          \
            --sysconfdir=%{_sysconfdir}      \
            --without-tcp-wrappers \
            --disable-nfsv4        \
            --disable-gss
make
%install
make DESTDIR=%{buildroot} install
%files
%defattr(-,root,root)
%{_libdir}/*
%{_datadir}/*
/sbin/*
%{_sbindir}/*
%{_sharedstatedir}/*
%changelog
*	Tue Jul 14 2015 Rongrong Qiu <rqiu@vmware.com> 1.3.2-1
-	Initial build.	First version
