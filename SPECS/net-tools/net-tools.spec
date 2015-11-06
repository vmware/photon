Summary:	Networking Tools
Name:		net-tools
Version:	1.60
Release:	3%{?dist}
License:	GPLv2+
URL:		http://net-tools.sourceforge.net
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://www.tazenda.demon.co.uk/phil/net-tools/%{name}-%{version}.tar.bz2
%define sha1 net-tools=944fb70641505d5d1139dba3aeb81ba124574b83
Patch0: 	http://www.linuxfromscratch.org/patches/blfs/6.3/net-tools-1.60-gcc34-3.patch
Patch1:		http://www.linuxfromscratch.org/patches/blfs/6.3/net-tools-1.60-kernel_headers-2.patch
Patch2:		http://www.linuxfromscratch.org/patches/blfs/6.3/net-tools-1.60-mii_ioctl-1.patch
Obsoletes:	inetutils 
Requires:	iputils 
%description
The Net-tools package is a collection of programs for controlling the network subsystem of the Linux kernel. 
%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%build
yes "" | make config
sed -i -e 's|HAVE_IP_TOOLS 0|HAVE_IP_TOOLS 1|g' \
       -e 's|HAVE_AFINET6 0|HAVE_AFINET6 1|g' \
       -e 's|HAVE_MII 0|HAVE_MII 1|g' config.h
sed -i -e 's|#define HAVE_HWSTRIP 1|#define HAVE_HWSTRIP 0|g' \
       -e 's|#define HAVE_HWTR 1|#define HAVE_HWTR 0|g' config.h
sed -i -e 's|# HAVE_IP_TOOLS=0|HAVE_IP_TOOLS=1|g' \
       -e 's|# HAVE_AFINET6=0|HAVE_AFINET6=1|g' \
       -e 's|# HAVE_MII=0|HAVE_MII=1|g' config.make
make
%install
make BASEDIR=%{buildroot} BINDIR=%{_bindir} SBINDIR=%{_sbindir} install
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/bin/*
/sbin/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
*	Fri Nov 6 2015 Alexey Makhalov <amakhalov@vmware.com> 1.60-4
-	Added ipv6 support. Include hostname and dnshostname.
*	Thu Oct 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.60-3
-	Added changes to replace inetutils with net-tools
*	Thu Jul 30 2015 Divya Thaluru <dthaluru@vmware.com> 1.60-2
-	Disable building with parallel threads
*	Mon Jul 13 2015 Divya Thaluru <dthaluru@vmware.com> 1.60-1
-	Initial build.	First version
