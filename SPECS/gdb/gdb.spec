Summary:        C debugger
Name:           gdb
Version:        10.1
Release:        5%{?dist}
License:        GPLv2+
URL:            http://www.gnu.org/software/%{name}
Source0:        http://ftp.gnu.org/gnu/gdb/%{name}-%{version}.tar.xz
%define sha512  gdb=0dc54380435c6853db60f1e388b94836d294dfa9ad7f518385a27db4edd03cb970f8717d5f1e9c9a0d4a33d7fcf91bc2e5d6c9cf9e4b561dcc74e65b806c1537
Source1:        gdbinit
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Patch0:         gdb-7.12-pstack.patch
Patch1:         0001-skip-inaccessible.patch
Patch2:         0001-CVE-2021-3549.patch
Patch3:         0001-CVE-2022-4285.patch
Patch4:         0001-CVE-2022-38533.patch
Patch5:         0001-CVE-2023-1972.patch
Patch6:         0001-CVE-2023-25584.patch
Patch7:         0001-CVE-2023-25585.patch
Patch8:         0001-CVE-2023-25588.patch
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
%{_libdir}/*.so
%{_infodir}/*.gz
%{_datadir}/gdb/python/*
%{_datadir}/gdb/syscalls/*
%{_datadir}/gdb/system-gdbinit/*
%{_bindir}/*
%{_mandir}/*/*
%{_sysconfdir}/gdbinit
%{_sysconfdir}/gdbinit.d

%changelog
* Fri Sep 22 2023 Anmol Jain <anmolja@vmware.com> 10.1-5
- Fix for CVE-2023-1972, CVE-2023-25584, CVE-2023-25585 & CVE-2023-25588
* Thu Aug 10 2023 Anmol Jain <anmolja@vmware.com> 10.1-4
- Fix for CVE-2021-3549, CVE-2022-38533 & CVE-2022-4285
* Wed Jul 12 2023 Anmol Jain <anmolja@vmware.com> 10.1-3
- Using system zlib to fix CVE-2018-25032
* Mon Feb 20 2023 Ajay Kaher <akaher@vmware.com> 10.1-2
- Compile with --with-system-gdbinit
* Tue Jan 03 2023 Harinadh D <hdommaraju@vmware.com> 10.1-1
- Version update to fix multiple CVE's in binutils
* Sun May 24 2020 Vikash Bansal <bvikas@vmware.com> 8.2-3
- Stop inaccessible region from getting dumped into coredump
* Fri Oct 18 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.2-2
- Fix CVE-2019-1010180
* Fri Sep 14 2018 Keerthana K <keerthanak@vmware.com> 8.2-1
- Update to version 8.2
* Thu Dec 07 2017 Alexey Makhalov <amakhalov@vmware.com> 7.12.1-8
- Enable LZMA support
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 7.12.1-7
- Aarch64 support
* Mon Sep 11 2017 Rui Gu <ruig@vmware.com> 7.12.1-6
- Enable make check in docker with part of checks disabled
* Thu Aug 10 2017 Alexey Makhalov <amakhalov@vmware.com> 7.12.1-5
- Make check improvements
* Fri Jul 21 2017 Rui Gu <ruig@vmware.com> 7.12.1-4
- Add pstack wrapper which will invoke gdb.
* Wed Jul 12 2017 Alexey Makhalov <amakhalov@vmware.com> 7.12.1-3
- Get tcl, expect and dejagnu from packages
* Thu May 18 2017 Xiaolin Li <xiaolinl@vmware.com> 7.12.1-2
- Build gdb with python3.
* Wed Mar 22 2017 Alexey Makhalov <amakhalov@vmware.com> 7.12.1-1
- Version update
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.8.2-3
- GA - Bump release of all rpms
* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 7.8.2-2
- Handled locale files with macro find_lang
* Wed Apr 08 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.8.2-1
- Initial build. First version
