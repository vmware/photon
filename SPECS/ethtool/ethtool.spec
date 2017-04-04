Summary:	ethtool is the standard Linux utility for controlling network drivers and hardware, particularly for wired Ethernet devices. 
Name:		ethtool
Version:	4.8
Release:	1%{?dist}
License:	GPLv2
URL:		https://www.kernel.org/pub/software/network/ethtool/
Group:		Productivity/Networking/Diagnostic
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://www.kernel.org/pub/software/network/%{name}/%{name}-%{version}.tar.gz
%define sha1 ethtool=6ae18bac4f3a66c458142d0c3c438ebade757afb
#BuildRequires: python2 python2-libs

%description
 ethtool is the standard Linux utility for controlling network drivers and hardware, particularly for wired Ethernet devices

%prep
%setup -q

%build
autoreconf -fi
#export CFLAGS="$RPM_OPT_FLAGS -W -Wall -Wstrict-prototypes -Wformat-security -Wpointer-arith"
./configure --prefix=%{_prefix} --sbindir=/sbin
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} check

%clean
rm -rf %{buildroot}/*

%files
%doc AUTHORS COPYING NEWS README ChangeLog
%defattr(-,root,root)
/sbin/*
%{_mandir}

%changelog
*	Mon Apr 03 2017 Chang Lee <changlee@vmware.com> 4.8-1
-	Upgraded to version 4.8
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2-3
-	GA - Bump release of all rpms
*   	Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 4.2-2
-   	Change file packaging.
*	Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2-1
-	Initial build.	First version
