Summary:	Utilities for block layer IO tracing
Name:		blktrace    
Version:	1.0.5
Release:	1%{?dist}
License:	GPLv2 
URL:		http://git.kernel.org/cgit/linux/kernel/git/axboe/blktrace.git/tree/README
Group:		Development/Tools/Other
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://blktrace.sourcearchive.com/downloads/1.0.5-1/%{name}-%{version}.orig.tar.gz
%define sha1 blktrace=f88072fc306adb595ebc7b33cc7ed4edb08a750f
BuildRequires: libaio-devel
Requires:	libaio

%description
 blktrace is a block layer IO tracing mechanism which provides detailed
information about request queue operations up to user space.
%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} prefix=%{_prefix} mandir=%{_mandir}

%clean
rm -rf %{buildroot}/*
 
%files
%doc README 
%defattr(-,root,root)
%{_bindir}
%{_mandir}

%changelog
*	Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0.5-1
-	Initial build.	First version
