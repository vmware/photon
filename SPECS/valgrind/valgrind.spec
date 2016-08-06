%global security_hardening none
Summary:	Memory Management Debugger.
Name:		valgrind
Version:	3.11.0
Release:	1%{?dist}
License:	GPLv2+
URL:		http://valgrind.org
Group:		Development/Debuggers
Source0:        http://valgrind.org/downloads/%{name}-%{version}.tar.bz2
%define sha1 valgrind=340757e91d9e83591158fe8bb985c6b11bc53de5
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:  pkg-config

%description
Valgrind is a GPL'd system for debugging and profiling Linux programs. With
Valgrind's tool suite you can automatically detect many memory management and
threading bugs, avoiding hours of frustrating bug-hunting, making your programs
more stable. You can also perform detailed profiling to help speed up your 
programs.

%prep
%setup -q -n %{name}-%{version}

%build
./configure --prefix=%{_prefix}
make

%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/valgrind
%{_libdir}/valgrind
%{_libdir}/pkgconfig/*
%{_mandir}/*/*
%{_datadir}/doc/valgrind/*

%changelog
*       Fri Aug 05 2016 Kumar Kaushik <kaushikk@vmware.com> 3.11.0-1
-       Initial Build.
