Name:           jemalloc
Version:        4.5.0
Release:        1%{?dist}
Summary:        A general purpose malloc implementation that emphasizes fragmentation avoidance and scalable concurrency support.
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
License:        BSD-2-Clause
URL:            https://github.com/jemalloc/jemalloc/
Source0:        https://github.com/jemalloc/jemalloc/releases/download/%{version}/%{name}-%{version}.tar.bz2
%define sha1 jemalloc=e7714d070c623bff9acf682e9d52c930e491acd8
BuildRequires:  bzip2 elfutils

%description
jemalloc is a general purpose malloc(3) implementation that emphasizes fragmentation avoidance
and scalable concurrency support. jemalloc first came into use as the FreeBSD libc allocator
in 2005, and since then it has found its way into numerous applications that rely on its
predictable behavior. In 2010 jemalloc development efforts broadened to include developer
support features such as heap profiling and extensive monitoring/tuning hooks. Modern jemalloc
releases continue to be integrated back into FreeBSD, and therefore versatility remains
critical. Ongoing development efforts trend toward making jemalloc among the best allocators
for a broad range of demanding applications, and eliminating/mitigating weaknesses that have
practical repercussions for real world applications.

%package devel
Summary:        Header and development files for jemalloc
Requires:       %{name} = %{version}

%description devel
jemalloc-devel package contains header files for jemalloc

%prep
%setup -q

%build
%configure
make %{?_smp_mflags}

%install
%make_install

%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%doc README INSTALL
%{_bindir}/%{name}.sh
%{_libdir}/*.so.*
%{_mandir}/*
%{_docdir}/*

%files devel
%{_bindir}/*
%exclude %{_bindir}/%{name}.sh
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/%{name}.pc

%changelog
*       Fri May 29 2020 Stanislav Hadjiiski <hadjiiskis@vmware.com> 4.5.0-1
-       Initial build
