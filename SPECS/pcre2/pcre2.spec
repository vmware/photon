Summary:        PCRE2 - Perl-Compatible Regular Experessions
Name:           pcre2
Version:        10.40
Release:        2%{?dist}
Url:            https://github.com/PhilipHazel/pcre2/
License:        BSD
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/PhilipHazel/pcre2/releases/download/pcre2-%{version}/%{name}-%{version}.tar.gz
%define sha512  %{name}=679c6f540571850adec880934812e4f26f08ad858c776f10d1ed68ed3c0d4f91f6e1b53d781b53340af43a22c521e585cfc908f3659013c630a320e4fb246dc2

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  readline-devel
BuildRequires:  bzip2-devel
BuildRequires:  glibc

Requires:       libgcc
Requires:       readline
Requires:       libstdc++
Requires:       pcre2-libs = %{version}-%{release}
Requires:       bzip2-libs

Patch0:         diagnose-negative-repeat-value-in-pcre2test-subj-line.patch

%description
The PCRE2 library is a set of C functions that implement regular expression pattern matching using the same syntax and semantics as Perl 5.
PCRE2 has its own native API, as well as a set of wrapper functions that correspond to the POSIX regular expression API.
It comes in three forms, for processing 8-bit, 16-bit, or 32-bit code units, in either literal or UTF encoding.

%package        devel
Summary:        Development files for libpcre2
Requires:       %{name} = %{version}-%{release}

%description    devel
All of the required files to develop with the pcre2 library

%package        libs
Summary:        Libraries for pcre2
Group:          System Environment/Libraries

%description    libs
This package contains minimal set of shared pcre libraries.

%prep
%autosetup -p1

%build
%configure \
            --enable-unicode-properties \
            --enable-utf \
            --enable-pcre2-8  \
            --enable-pcre2-16 \
            --enable-pcre2-32 \
            --enable-pcregrep-libz \
            --enable-pcregrep-libbz2 \
            --enable-pcretest-libreadline \
            --enable-shared \
            --disable-static
%make_build

%install
%make_install %{?_smp_mflags}

%if 0%{?with_check}
%check
%make_build check
%endif

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%exclude %dir %{_libdir}/debug
%{_bindir}/pcre2grep
%{_bindir}/pcre2-config

%files devel
%defattr(-, root, root)
%exclude %{_defaultdocdir}/%{name}*/*
%exclude %{_mandir}/*/*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_bindir}/pcre2test
%{_libdir}/*.so

%files libs
%defattr(-, root, root)
%{_libdir}/*.so.*

%changelog
*   Mon Jul 24 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 10.40-2
-   Fix for CVE-2022-41409.
*   Fri Sep 23 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 10.40-1
-   Initial addition of pcre2. Needed for SSSD.
