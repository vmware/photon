Summary:	Sysdig is a universal system visibility tool with native support for containers.
Name:		sysdig
Version:	0.8.0
Release:	1%{?dist}
License:	GPLv2	  
URL:		http://www.sysdig.org/
Group:		Applications/System	
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/draios/sysdig/archive/%{name}-%{version}.tar.gz
%define sha1 sysdig=22a9102ff238a8feeaa4ecbcd54a29aa8b7e4cb8
BuildRequires: cmake linux-dev 

%description
 Sysdig is open source, system-level exploration: capture system state and activity from a running Linux instance, then save, filter and analyze. Sysdig is scriptable in Lua and includes a command line interface and a powerful interactive UI, csysdig, that runs in your terminal

%prep
%setup -q

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -DBUILD_DRIVER=OFF ..
make 

%install
cd build
make install DESTDIR=%{buildroot}


mv %{buildroot}/usr/src/sysdig* %{buildroot}/usr/src/sysdig-%{version}
mkdir -p %{buildroot}/etc/
mv %{buildroot}/usr/etc/bash_completion.d %{buildroot}/etc/
rm -rf %{buildroot}/usr/share/zsh/

%clean
rm -rf %{buildroot}/*
 
%files
%defattr(-,root,root)
/etc/bash_completion.d/* 
%{_bindir}
/usr/src 
%{_datadir}

%changelog
*       Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 0.8.0-1
-       Upgraded to new version.
*   	Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 0.6.0-1
-   	Upgrade version.
*	Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.1.101-1
-	Initial build.	First version
