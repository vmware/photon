Summary:	Tracks system calls that are made by a running process
Name:		strace
Version:	4.11
Release:	3%{?dist}
License:	BSD
URL:		http://sourceforge.net/p/strace/code/ci/master/tree/
Group:		Development/Debuggers
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://downloads.sourceforge.net/project/strace/strace/%{version}/%{name}-%{version}.tar.xz
%define sha1 strace=8fd717dc3c51b69fde51ce0bdb066404a678363c
BuildRequires:	libacl-devel, libaio-devel
%global __requires_exclude ^/usr/bin/perl$

%description
The strace program intercepts and displays the system calls made by a running process. strace also records 
all the arugments and return values from the system calls. This is useful in debugging a process. 

%prep
%setup -q
%build

./configure \
	--prefix=%{_prefix} \

make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot}

%check
make -k check 

%clean
rm -rf %{buildroot}/*

%files 
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%changelog
*	Thu Oct 20 2016 Alexey Makhalov <amakhalov@vmware.com> 4.11-3
-	Exclude perl dependency
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.11-2
-	GA - Bump release of all rpms
*   	Wed Jan 20 2016 Anish Swaminathan <anishs@vmware.com> 4.11-1
-   	Upgrade version.
*	Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 4.10-1
-	Initial build.	First version
