Summary:        PCRE2 - Perl-Compatible Regular Experessions
Name:           pcre2
Version:        10.42
Release:        2%{?dist}
Url:            https://github.com/PhilipHazel/pcre2
License:        BSD
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/PhilipHazel/pcre2/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}=a3db6c5c620775838819be616652e73ce00f5ef5c1f49f559ff3efb51a119d02f01254c5901c1f7d0c47c0ddfcf4313e38d6ca32c35381b8f87f36896d10e6f7

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  (coreutils or coreutils-selinux)
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
* Fri Nov 24 2023 Shreenidhi Shedi <sshedi@vmware.com> 10.42-2
- Enable jit support, needed by syslog-ng
* Mon Jul 24 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 10.42-1
- Update to latest version, fix minor CVE
* Tue Jan 31 2023 Shreenidhi Shedi <sshedi@vmware.com> 10.40-3
- Fix file packaging
* Tue Dec 20 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 10.40-2
- Bump release as a part of readline upgrade
* Wed Jun 01 2022 Gerrit Photon <photon-checkins@vmware.com> 10.40-1
- Automatic Version Bump
* Fri Mar 25 2022 Brennan Lamoreaux <blamoreaux@vmware.com> 10.39-1
- Initial addition of pcre2 - needed for building libnetconf2.
- Modified from photon/SPECS/pcre.spec for pcre2.
