Summary:        PCRE2 - Perl-Compatible Regular Experessions
Name:           pcre2
Version:        10.40
Release:        7%{?dist}
Url:            https://github.com/PhilipHazel/pcre2
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/PhilipHazel/pcre2/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=679c6f540571850adec880934812e4f26f08ad858c776f10d1ed68ed3c0d4f91f6e1b53d781b53340af43a22c521e585cfc908f3659013c630a320e4fb246dc2

Source1: license.txt
%include %{SOURCE1}

Patch0: diagnose-negative-repeat-value-in-pcre2test-subj-line.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils >= 9.1-7
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  readline-devel
BuildRequires:  bzip2-devel
BuildRequires:  glibc

Requires:       libgcc
Requires:       readline
Requires:       libstdc++
Requires:       %{name}-libs = %{version}-%{release}
Requires:       bzip2-libs

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
    --docdir=%{_docdir}/%{name}-%{version} \
    --enable-unicode-properties \
    --enable-utf \
    --enable-%{name}-8  \
    --enable-%{name}-16 \
    --enable-%{name}-32 \
    --enable-pcregrep-libz \
    --enable-pcregrep-libbz2 \
    --enable-pcretest-libreadline \
    --enable-shared \
    --disable-static \
    --enable-jit

%make_build

%install
%make_install %{?_smp_mflags}

%check
%make_build check

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%exclude %dir %{_libdir}/debug
%{_bindir}/pcre2grep
%{_bindir}/%{name}-config

%files devel
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}/*
%{_mandir}/*/*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_bindir}/pcre2test
%{_libdir}/*.so

%files libs
%defattr(-,root,root)
%{_libdir}/*.so.*

%changelog
* Fri Nov 08 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 10.40-7
- Remove standalone license exceptions
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 10.40-6
- Release bump for SRP compliance
* Fri Nov 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 10.40-5
- Enable jit support, needed by syslog-ng
* Mon Jul 24 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 10.40-4
- Fix for CVE-2022-41409
* Tue Jan 31 2023 Shreenidhi Shedi <sshedi@vmware.com> 10.40-3
- Fix file packaging
* Tue Dec 20 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 10.40-2
- Bump release as a part of readline upgrade
* Wed Jun 01 2022 Gerrit Photon <photon-checkins@vmware.com> 10.40-1
- Automatic Version Bump
* Fri Mar 25 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 10.39-1
- Initial addition of pcre2 - needed for building libnetconf2.
- Modified from photon/SPECS/pcre.spec for pcre2.
