Summary:	The GNU portable thread library.
Name:		pth
Version:	2.0.7
Release:	1%{?dist}
License:	LGPLv2+
URL:		http://www.gnu.org/software/pth/
Group:		System Environment/Libraries.
Source0:        http://open-source-box.org/%{name}/%{name}-%{version}.tar.gz
%define sha1 pth=9a71915c89ff2414de69fe104ae1016d513afeee
Vendor:		VMware, Inc.
Distribution:	Photon

%description

Pth is a very portable POSIX/ANSI-C based library for Unix platforms which 
provides non-preemptive priority-based scheduling for multiple threads of 
execution (aka ``multithreading'') inside event-driven applications. All
threads run in the same address space of the server application, but each
thread has it's own individual program-counter, run-time stack, signal
mask and errno variable.

%package devel
Summary:       GNU pth development header and libraries.
Group:         Development/Libraries.
Requires:      pth = %{version}

%description devel
Development package for pth.

%prep
%setup -q

%build
%configure --disable-static \
           --prefix=%{_prefix}
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*.so
%{_mandir}/*/*
%{_datadir}/aclocal/*

%changelog
*       Wed Jul 27 2016 Kumar Kaushik <kaushikk@vmware.com> 2.0.7-1
-       Initial Build.
