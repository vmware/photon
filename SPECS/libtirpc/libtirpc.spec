Summary:	libtirpc
Name:		libtirpc
Version:	0.3.2
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.linuxfromscratch.org/
Group:		Applications/Libtirpc
Source0:	http://downloads.sourceforge.net/project/libtirpc/libtirpc/0.3.2/%{name}-%{version}.tar.bz2
%define sha1 libtirpc =af9b74d0c4d1499a7b1a43e396e5b7d62180ea65
Patch0:          libtirpc-0.3.2-api_fixes-1.patch  
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:  krb5
BuildRequires:  automake

%description
The libtirpc package contains a small, simple rpc service

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%build

./configure --prefix=%{_prefix}     \
            --sysconfdir=%{_sysconfdir} \
            --disable-static  \
            --disable-gssapi
make
%install
make DESTDIR=%{buildroot} install
#mkdir %{buildroot}/lib
#mv -v %{buildroot}/usr/lib/libtirpc.so.* %{buildroot}/lib
#ln -sfv ../../lib/libtirpc.so.1.0.10 %{buildroot}/usr/lib/libtirpc.so
%files
%defattr(-,root,root)
%{_libdir}/*
#%{_lib}/*
%{_sysconfdir}/*
%{_includedir}/*
%{_datadir}/*
%changelog
*	Tue Jul 14 2015 Rongrong Qiu <rqiu@vmware.com> 0.3.2-1
-	Initial build.	First version
