Summary:	Nfs service
Name:		nfs-utils
Version:	1.3.2
Release:	1
License:	GPLv3+
URL:		http://www.linuxfromscratch.org/
Group:		Applications/Nfs-server
Source0:	%{name}-%{version}.tar.bz2
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires: krb5
BuildRequires: libtirpc
Requires: libtirpc
Requires: python2-libs

%description
The nfs package contains a small, simple nfs service

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
*	Wed Jul 1 2015 Rongrong Qiu <rqiu@vmware.com> 1.3.2-1
-	Initial build.	First version
