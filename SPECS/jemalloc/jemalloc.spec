Name:           jemalloc
Version:        5.3.0
Release:        2%{?dist}
Summary:        A general purpose malloc implementation that emphasizes fragmentation avoidance and scalable concurrency support.
Group:          System Environment/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://github.com/jemalloc/jemalloc/
Source0:        https://github.com/jemalloc/jemalloc/releases/download/%{version}/%{name}-%{version}.tar.bz2
%define sha512  jemalloc=22907bb052096e2caffb6e4e23548aecc5cc9283dce476896a2b1127eee64170e3562fa2e7db9571298814a7a2c7df6e8d1fbe152bd3f3b0c1abec22a2de34b1

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  bzip2

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
%autosetup

%build
%configure
make %{?_smp_mflags}

%install
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%doc README
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
*       Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 5.3.0-2
-       Release bump for SRP compliance
*       Thu May 26 2022 Gerrit Photon <photon-checkins@vmware.com> 5.3.0-1
-       Automatic Version Bump
*       Thu Jul 23 2020 Gerrit Photon <photon-checkins@vmware.com> 5.2.1-1
-       Automatic Version Bump
*       Wed Sep 4 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 4.5.0-2
-       Enabled build for non x86_64 build archs
*       Fri Aug 23 2019 Stanislav Hadjiiski <hadjiiskis@vmware.com> 4.5.0-1
-       Initial build
