%global build_minimal_gdb 1

Summary:        C debugger
Name:           gdb
Version:        11.2
Release:        7%{?dist}
License:        GPLv2+
URL:            http://www.gnu.org/software/%{name}
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.gnu.org/gnu/gdb/%{name}-%{version}.tar.xz
%define sha512  %{name}=07e9026423438049b11f4f784d57401ece4e940570f613bd6958b3714fe7fbc2c048470bcce3e7d7d9f93331cdf3881d30dcc964cb113a071143a02b28e5b127

Source1:        gdbinit

Patch0:         gdb-7.12-pstack.patch
Patch1:         gdb-Stop-inaccessible-region-from-getting-dumped.patch

Requires:       expat
Requires:       ncurses
Requires:       python3
Requires:       xz-libs

BuildRequires:  expat-devel
BuildRequires:  ncurses-devel
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  xz-devel

%if 0%{?with_check}
BuildRequires:  dejagnu
BuildRequires:  systemtap-sdt-devel
%endif

%description
GDB, the GNU Project debugger, allows you to see what is going on
`inside' another program while it executes -- or what
another program was doing at the moment it crashed.

%if 0%{?build_minimal_gdb}
%package minimal
Summary: A GNU source-level debugger for C, C++, Fortran, Go and other languages (minimal version)
Conflicts: %{name} < %{version}-%{release}

%description minimal
GDB, the GNU debugger, allows you to debug programs written in C, C++, Java, and other languages,
by executing them in a controlled fashion and printing their data.
This package provides a minimal version of GDB, tailored to be used by the Photon buildroot.
It should probably not be used by end users.
%endif

%prep
%autosetup -p1

%build
mkdir -p build && cd build
sh ../configure \
  --host=%{_host} --build=%{_build} \
  --prefix=%{_prefix} \
  --with-system-gdbinit=%{_sysconfdir}/gdbinit \
  --with-python=%{_bindir}/python3

make %{?_smp_mflags}

%if 0%{?build_minimal_gdb}
cd ../ && mkdir -p minimal-build && cd minimal-build
sh ../configure \
  --host=%{_host} --build=%{_build} --prefix=%{_prefix} \
  --without-babeltrace \
  --without-expat \
  --disable-tui \
  --without-python \
  --without-guile \
  --disable-inprocess-agent \
  --without-intel-pt \
  --disable-unit-tests \
  --disable-source-highlight

make %{?_smp_mflags}
%endif

%install
cd build && make DESTDIR=%{buildroot} install %{?_smp_mflags}
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

%if 0%{?build_minimal_gdb}
mkdir -p %{buildroot}/minimal-gdb
cd ../minimal-build && make DESTDIR=%{buildroot}/minimal-gdb install %{?_smp_mflags}

rm -rfv %{buildroot}/minimal-gdb%{_prefix}/{include,lib*,share} \
       %{buildroot}/minimal-gdb%{_bindir}/{gcore,gdbserver,gstack,gdb-add-index,pstack,run}

mv %{buildroot}/minimal-gdb%{_bindir}/gdb %{buildroot}%{_bindir}/gdb.minimal
%endif

%ifarch aarch64
rm %{buildroot}%{_libdir}/libaarch64-unknown-linux-gnu-sim.a
%endif

%find_lang %{name} --all-name ../%{name}.lang
mkdir -p %{buildroot}%{_sysconfdir}/gdbinit.d
install -m 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/gdbinit

%check
%if 0%{?with_check}
# disable security hardening for tests
rm -f $(dirname $(gcc -print-libgcc-file-name))/../specs
# fix typo in test
sed -i 's/hex in)/hex in )/g' gdb/testsuite/gdb.arch/i386-signal.exp
# ignore exit code and check for expected number of failures
make %{?_smp_mflags} check || tail gdb/testsuite/gdb.sum  | grep "# of unexpected failures.*1219\|# of unexpected failures.*1220"
%endif

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
%{_sysconfdir}/gdbinit
%{_sysconfdir}/gdbinit.d

%if 0%{?build_minimal_gdb}
%files minimal
%defattr(-,root,root)
%{_bindir}/gdb.minimal
%{_bindir}/gdb-add-index
%endif

%changelog
* Fri Jun 09 2023 Nitesh Kumar <kunitesh@vmware.com> 11.2-7
- Bump version as a part of ncurses upgrade to v6.4
* Mon Feb 27 2023 Ajay Kaher <akaher@vmware.com> 11.2-6
- Compile with --with-system-gdbinit
* Fri Dec 23 2022 Oliver Kurth <okurth@vmware.com> 11.2-5
- bump version as a part of xz upgrade
* Wed Dec 07 2022 Shivani Agarwal <shivania2@vmware.com> 11.2-4
- Bump version as a part of python upgrade
* Fri Dec 02 2022 Srinidhi Rao <srinidhir@vmware.com> 11.2-3
- Bump version as a part of systemtap upgrade
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 11.2-2
- Add gdb-minimal sub package
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 11.2-1
- Automatic Version Bump
* Mon May 03 2021 Gerrit Photon <photon-checkins@vmware.com> 10.2-1
- Automatic Version Bump
* Thu Jan 07 2021 Tapas Kundu <tkundu@vmware.com> 10.1-1
- Update to version 10.1
* Tue Jan 05 2021 Tapas Kundu <tkundu@vmware.com> 9.2-3
- Fix compatibility with python 3.9
* Mon Oct 05 2020 Vikash Bansal <bvikas@vmware.com> 9.2-2
- Stop inaccessible region from getting dumped into coredump
* Mon Aug 24 2020 Keerthana K <keerthanak@vmware.com> 9.2-1
- Update to version 9.2
* Mon Jul 22 2019 Alexey Makhalov <amakhalov@vmware.com> 8.2-2
- Cross compilation support
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
