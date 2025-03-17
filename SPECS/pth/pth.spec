Summary:    The GNU portable thread library.
Name:       pth
Version:    2.0.7
Release:    2%{?dist}
URL:        http://www.gnu.org/software/pth/
Group:      System Environment/Libraries.
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:        http://open-source-box.org/%{name}/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
Requires:      %{name} = %{version}-%{release}

%description devel
Development package for pth.

%prep
%autosetup -p1

%build
%configure --disable-static

# make doesn't support _smp_mflags
make

%install
%make_install

%check
%make_build check

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
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.7-2
- Release bump for SRP compliance
* Wed Jul 27 2016 Kumar Kaushik <kaushikk@vmware.com> 2.0.7-1
- Initial Build.
