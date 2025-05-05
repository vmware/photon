Summary:        C debugger
Name:           gdb
Version:        13.2
Release:        4%{?dist}
License:        GPLv2+
URL:            http://www.gnu.org/software/%{name}
Source0:        http://ftp.gnu.org/gnu/gdb/%{name}-%{version}.tar.xz
%define sha512 %{name}=8185d3e11ab60dafff5860a5016577bfe7dd7547ef01ebc867bc247603d82b74ff74c4f29492c7d2aee57076f52be33e289f4c6b414a4b870d4b3004909f4c34

Source1:        gdbinit
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Patch0:         CVE-2023-1972.patch
Requires:       expat
Requires:       ncurses
Requires:       python3
Requires:       xz-libs
Requires:       zlib
BuildRequires:  expat-devel
BuildRequires:  ncurses-devel
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires:  texinfo

%if 0%{?with_check}
BuildRequires:  dejagnu
BuildRequires:  systemtap-sdt-devel
%endif

%description
GDB, the GNU Project debugger, allows you to see what is going on
`inside' another program while it executes -- or what
another program was doing at the moment it crashed.
%prep
%autosetup -p1

%build
rm -rf zlib texinfo
mkdir build && cd build
../configure \
  --host=%{_host} --build=%{_build} \
  --prefix=%{_prefix} \
  --with-system-gdbinit=%{_sysconfdir}/gdbinit \
  --with-python=/usr/bin/python3 \
  --with-system-zlib

%make_build

%install
cd build && make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
rm %{buildroot}%{_infodir}/dir \
   %{buildroot}%{_libdir}/libctf-nobfd.a \
   %{buildroot}%{_libdir}/libctf.a

# following files conflicts with binutils-2.24-1.x86_64
rm %{buildroot}%{_includedir}/ansidecl.h \
   %{buildroot}%{_includedir}/bfd.h \
   %{buildroot}%{_includedir}/bfdlink.h \
   %{buildroot}%{_includedir}/dis-asm.h \
   %{buildroot}%{_libdir}/libbfd.a \
   %{buildroot}%{_libdir}/libopcodes.a

# following files conflicts with binutils-2.25-1.x86_64
rm %{buildroot}%{_datadir}/locale/de/LC_MESSAGES/opcodes.mo \
   %{buildroot}%{_datadir}/locale/fi/LC_MESSAGES/bfd.mo \
   %{buildroot}%{_datadir}/locale/fi/LC_MESSAGES/opcodes.mo

%find_lang %{name} --all-name ../%{name}.lang
mkdir -p %{buildroot}%{_sysconfdir}/gdbinit.d
install -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/gdbinit

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
%{_libdir}/libsframe.a
%{_libdir}/*.so
%{_infodir}/*.gz
%{_datadir}/gdb/python/*
%{_datadir}/gdb/syscalls/*
%{_datadir}/gdb/system-gdbinit/*
%{_bindir}/*
%{_mandir}/*/*
%{_sysconfdir}/gdbinit
%{_sysconfdir}/gdbinit.d
%ifarch aarch64
%{_includedir}/sim/callback.h
%{_includedir}/sim/sim.h
%{_libdir}/libsim.a
%endif

%changelog
*   Mon May 05 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 13.2-4
-   Version bump for expat upgrade
*   Thu Feb 29 2024 Anmol Jain <anmol.jain@broadcom.com> 13.2-3
-   Bump version as a part of expat upgrade
*   Fri Oct 20 2023 Anmol Jain <anmolja@vmware.com> 13.2-2
-   Fix for CVE-2023-1972
*   Tue Jul 25 2023 Anmol Jain <anmolja@vmware.com> 13.2-1
-   Version upgrade
*   Mon Feb 27 2023 Ajay Kaher <akaher@vmware.com> 10.1-3
-   Compile with --with-system-gdbinit
*   Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 10.1-2
-   Bump up to compile with python 3.10
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
