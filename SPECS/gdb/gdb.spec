Summary:        C debugger
Name:           gdb
Version:        11.2
Release:        1%{?dist}
License:        GPLv2+
URL:            http://www.gnu.org/software/%{name}
Source0:        http://ftp.gnu.org/gnu/gdb/%{name}-%{version}.tar.xz
%define sha512  gdb=07e9026423438049b11f4f784d57401ece4e940570f613bd6958b3714fe7fbc2c048470bcce3e7d7d9f93331cdf3881d30dcc964cb113a071143a02b28e5b127
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       expat
Requires:       ncurses
Requires:       python3
Requires:       xz-libs
BuildRequires:  expat-devel
BuildRequires:  ncurses-devel
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  xz-devel
%if %{with_check}
BuildRequires:  dejagnu
BuildRequires:  systemtap-sdt-devel
%endif

%description
GDB, the GNU Project debugger, allows you to see what is going on
`inside' another program while it executes -- or what
another program was doing at the moment it crashed.
%prep
%autosetup

%build
mkdir build && cd build
../configure \
  --host=%{_host} --build=%{_build} \
  --prefix=%{_prefix} \
  --with-python=/usr/bin/python3
make %{?_smp_mflags}

%install
cd build && make DESTDIR=%{buildroot} %{?_smp_mflags} install
find %{buildroot} -name '*.la' -delete
rm %{buildroot}%{_infodir}/dir
rm %{buildroot}%{_libdir}/libctf-nobfd.a
rm %{buildroot}%{_libdir}/libctf.a

# following files conflicts with binutils-2.24-1.x86_64
rm %{buildroot}%{_includedir}/ansidecl.h
rm %{buildroot}%{_includedir}/bfd.h
rm %{buildroot}%{_includedir}/bfdlink.h
rm %{buildroot}%{_includedir}/dis-asm.h
rm %{buildroot}%{_libdir}/libbfd.a
rm %{buildroot}%{_libdir}/libopcodes.a
# following files conflicts with binutils-2.25-1.x86_64
rm %{buildroot}%{_datadir}/locale/de/LC_MESSAGES/opcodes.mo
rm %{buildroot}%{_datadir}/locale/fi/LC_MESSAGES/bfd.mo
rm %{buildroot}%{_datadir}/locale/fi/LC_MESSAGES/opcodes.mo
%ifarch aarch64
rm %{buildroot}%{_libdir}/libaarch64-unknown-linux-gnu-sim.a
%endif
%find_lang %{name} --all-name ../%{name}.lang

%check
# disable security hardening for tests
rm -f $(dirname $(gcc -print-libgcc-file-name))/../specs
# fix typo in test
sed -i 's/hex in)/hex in )/g' gdb/testsuite/gdb.arch/i386-signal.exp
# ignore exit code and check for expected number of failures
make %{?_smp_mflags} check || tail gdb/testsuite/gdb.sum  | grep "# of unexpected failures.*1219\|# of unexpected failures.*1220"

%files -f %{name}.lang
%defattr(-,root,root)
%exclude %{_datadir}/locale
%exclude %{_includedir}/*.h
%{_includedir}/gdb/*.h
%{_includedir}/sim/*.h
%{_libdir}/*.so
%{_infodir}/*.gz
%{_datadir}/gdb/python/*
%{_datadir}/gdb/syscalls/*
%{_datadir}/gdb/system-gdbinit/*
%{_bindir}/*
%{_mandir}/*/*

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 11.2-1
-   Automatic Version Bump
*   Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 10.2-1
-   Automatic Version Bump
*   Thu Jan 07 2021 Tapas Kundu <tkundu@vmware.com> 10.1-1
-   Update to version 10.1
*   Tue Jan 05 2021 Tapas Kundu <tkundu@vmware.com> 9.2-3
-   Fix compatibility with python 3.9
*   Mon Oct 05 2020 Vikash Bansal <bvikas@vmware.com> 9.2-2
-   Stop inaccessible region from getting dumped into coredump
*   Mon Aug 24 2020 Keerthana K <keerthanak@vmware.com> 9.2-1
-   Update to version 9.2
*   Mon Jul 22 2019 Alexey Makhalov <amakhalov@vmware.com> 8.2-2
-   Cross compilation support
*   Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 8.2-1
-   Update to version 8.2
*   Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 7.12.1-8
-   Enable LZMA support
*   Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 7.12.1-7
-   Aarch64 support
*   Mon Sep 11 2017 Rui Gu <ruig@vmware.com> 7.12.1-6
-   Enable make check in docker with part of checks disabled
*   Thu Aug 10 2017 Alexey Makhalov <amakhalov@vmware.com> 7.12.1-5
-   Make check improvements
*   Fri Jul 21 2017 Rui Gu <ruig@vmware.com> 7.12.1-4
-   Add pstack wrapper which will invoke gdb.
*   Wed Jul 12 2017 Alexey Makhalov <amakhalov@vmware.com> 7.12.1-3
-   Get tcl, expect and dejagnu from packages
*   Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 7.12.1-2
-   Build gdb with python3.
*   Wed Mar 22 2017 Alexey Makhalov <amakhalov@vmware.com> 7.12.1-1
-   Version update
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.8.2-3
-   GA - Bump release of all rpms
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 7.8.2-2
-   Handled locale files with macro find_lang
*   Wed Apr 08 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.8.2-1
-   Initial build. First version
