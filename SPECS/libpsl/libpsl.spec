Summary:    libpsl - C library to handle the Public Suffix List
Name:       libpsl
Version:    0.21.1
Release:    1%{?dist}
License:    MIT
URL:        https://github.com/rockdaboot/libpsl
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    https://github.com/rockdaboot/libpsl/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha1 libpsl=dc5fd26d060b3445386b5a82628df900567654f4

BuildRequires: icu-devel
BuildRequires: python3
Requires:      icu

%description
libpsl is a C library to handle the Public Suffix List. A "public suffix" is a
domain name under which Internet users can directly register own names.

Browsers and other web clients can use it to

- Avoid privacy-leaking "supercookies";
- Avoid privacy-leaking "super domain" certificates;
- Domain highlighting parts of the domain in a user interface;
- Sorting domain lists by site;

Libpsl...

- has built-in PSL data for fast access;
- allows to load PSL data from files;
- checks if a given domain is a "public suffix";
- provides immediate cookie domain verification;
- finds the longest public part of a given domain;
- finds the shortest private part of a given domain;
- works with international domains (UTF-8 and IDNA2008 Punycode);
- is thread-safe;
- handles IDNA2008 UTS#46;

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains libraries and header files for
developing applications that use %{name}.

%package -n     psl
Summary:        Commandline utility to explore the Public Suffix List
Requires:       %{name} = %{version}-%{release}

%description -n psl
This package contains a commandline utility to explore the Public Suffix List,
for example it checks if domains are public suffixes, checks if cookie-domain
is acceptable for domains and so on.

%prep
%setup -q

%build
sed -i 's/env python/&3/' src/psl-make-dafsa
%configure --disable-silent-rules \
           --disable-static
make %{?_smp_mflags}

%install
%make_install
install -m0755 src/psl-make-dafsa %{buildroot}%{_bindir}/

%check
make check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n psl
%defattr(-,root,root)
%doc AUTHORS NEWS
%{_bindir}/psl
%{_bindir}/psl-make-dafsa
%{_mandir}/man1/psl.*
%{_mandir}/man1/psl-make-dafsa.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*

%changelog
*   Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 0.21.1-1
-   Automatic Version Bump
*   Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 0.21.0-1
-   Update to 0.21.0
-   Build with python3
-   Mass removal python2
*   Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 0.20.2-2
-   Added BuildRequires python2
*   Mon Sep 17 2018 Bo Gan <ganb@vmware.com> 0.20.2-1
-   Initial packaging of libpsl
