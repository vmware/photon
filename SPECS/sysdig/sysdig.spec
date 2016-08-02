%global security_hardening none
Summary:	Sysdig is a universal system visibility tool with native support for containers.
Name:		sysdig
Version:	0.10.1
Release:	2%{?kernelsubrelease}{?dist}
License:	GPLv2	  
URL:		http://www.sysdig.org/
Group:		Applications/System	
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/draios/sysdig/archive/%{name}-%{version}.tar.gz
%define sha1 sysdig=272b95ad02be4d194bba66d360ff935084d9c842
BuildRequires:	cmake 
BuildRequires:  linux-dev = %{KERNEL_VERSION}-%{KERNEL_RELEASE}
BuildRequires:	openssl-devel
BuildRequires:	curl
BuildRequires:	zlib-devel
BuildRequires:	ncurses-devel
Requires:   linux = %{KERNEL_VERSION}-%{KERNEL_RELEASE}
Requires:	zlib
Requires:	ncurses
Requires:	openssl
Requires:	curl

%description
 Sysdig is open source, system-level exploration: capture system state and activity from a running Linux instance, then save, filter and analyze. Sysdig is scriptable in Lua and includes a command line interface and a powerful interactive UI, csysdig, that runs in your terminal

%prep
%setup -q

%build
mkdir build
cd build

cmake \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DUSE_BUNDLED_OPENSSL=OFF \
	-DUSE_BUNDLED_CURL=OFF \
	-DUSE_BUNDLED_ZLIB=OFF \
	-DUSE_BUNDLED_NCURSES=OFF ..

make KERNELDIR="/lib/modules/%{KERNEL_VERSION}/build" 

%install
cd build
make install DESTDIR=%{buildroot} KERNELDIR="/lib/modules/%{KERNEL_VERSION}/build"
mv %{buildroot}/usr/src/sysdig* %{buildroot}/usr/src/sysdig-%{version}
mkdir -p %{buildroot}/etc/
mv %{buildroot}/usr/etc/bash_completion.d %{buildroot}/etc/
rm -rf %{buildroot}/usr/share/zsh/
mkdir -p %{buildroot}/lib/modules/%{KERNEL_VERSION}/extra
mv driver/sysdig-probe.ko %{buildroot}/lib/modules/%{KERNEL_VERSION}/extra

%clean
rm -rf %{buildroot}/*

%post
/sbin/depmod -a

%postun
/sbin/depmod -a
 
%files
%defattr(-,root,root)
/etc/bash_completion.d/* 
%{_bindir}
/usr/src 
%{_datadir}
/lib/modules/%{KERNEL_VERSION}/extra/sysdig-probe.ko

%changelog
*   Mon Aug 1 2016 Divya Thaluru <dthaluru@vmware.com> 0.10.1-2
-   Added kernel macros
*	Thu Jul 14 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.10.1-2
-	Updated sysdig to build the kernel module 
*       Tue Jun 28 2016 Anish Swaminathan <anishs@vmware.com> 0.10.1-1
-       Upgrade sysdig to 0.10.1
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.8.0-4
-	GA - Bump release of all rpms
*       Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 0.8.0-3
-	Removing usage of bundled packages to build sysdig package
*       Wed Mar 16 2016 Anish Swaminathan <anishs@vmware.com> 0.8.0-2
-       Add openssl to buildrequires.
*       Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 0.8.0-1
-       Upgraded to new version.
*   	Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 0.6.0-1
-   	Upgrade version.
*	Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.1.101-1
-	Initial build.	First version
