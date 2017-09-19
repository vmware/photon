%global security_hardening none
Summary:        Memory Management Debugger.
Name:           valgrind
Version:        3.12.0
Release:        2%{?dist}
License:        GPLv2+
URL:            http://valgrind.org
Group:          Development/Debuggers
Source0:        http://valgrind.org/downloads/%{name}-%{version}.tar.bz2
Patch0:         fix-test-stack_changes.patch
%define sha1    valgrind=7a6878bf998c60d1e377a4f22ebece8d9305bda4
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  pkg-config

%description
Valgrind is a GPL'd system for debugging and profiling Linux programs. With
Valgrind's tool suite you can automatically detect many memory management and
threading bugs, avoiding hours of frustrating bug-hunting, making your programs
more stable. You can also perform detailed profiling to help speed up your 
programs.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
./configure --prefix=%{_prefix}
make

%install
make DESTDIR=%{buildroot} install

%check
make %{?_smp_mflags} -k check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/valgrind
%{_libdir}/valgrind
%{_libdir}/pkgconfig/*
%{_mandir}/*/*
%{_datadir}/doc/valgrind/*

%changelog
*   Tue Sep 19 2017 Bo Gan <ganb@vmware.com> 3.12.0-2
-   Fix make check issue
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.12.0-1
-   Updated to version 3.12.0.
*   Fri Aug 05 2016 Kumar Kaushik <kaushikk@vmware.com> 3.11.0-1
-   Initial Build.
