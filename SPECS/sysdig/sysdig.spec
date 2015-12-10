Summary:	Sysdig is a universal system visibility tool with native support for containers.
Name:		sysdig
Version:	0.1.101
Release:	2%{?dist}
License:	GPLv2	  
URL:		http://www.sysdig.org/
Group:		Applications/System	
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/draios/sysdig//archive/sysdig-0.1.101.tar.gz
%define sha1 sysdig=767de8855fcd18d06af6c7e8197001987e70bacc
BuildRequires: cmake linux-dev 

%description
 Sysdig is open source, system-level exploration: capture system state and activity from a running Linux instance, then save, filter and analyze. Sysdig is scriptable in Lua and includes a command line interface and a powerful interactive UI, csysdig, that runs in your terminal

%prep
%setup -q

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -DBUILD_DRIVER=OFF ..
make %{?_smp_mflags}

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
%{_sysconfdir}/bash_completion.d/*
%{_bindir}
/usr/src 
%{_datadir}

%changelog
*	Wed Dec 09 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> 0.1.101-2
-	Updating the provided files by the package.

*	Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.1.101-1
-	Initial build.	First version
