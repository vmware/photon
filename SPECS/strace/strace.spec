Summary:	Tracks system calls that are made by a running process
Name:		strace
Version:	4.10
Release:	1%{?dist}
License:	BSD
URL:		http://sourceforge.net/p/strace/code/ci/master/tree/
Group:		Development/Debuggers
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://downloads.sourceforge.net/project/strace/strace/4.10/%{name}-%{version}.tar.xz
%define sha1 strace=5c3ec4c5a9eeb440d7ec70514923c2e7e7f9ab6c
BuildRequires:	libacl-devel, libaio-devel

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
*	Thu Oct 09 2014 Divya Thaluru <dthaluru@vmware.com> 1.8.11p1-1
-	Initial build.	First version
