Summary:        C debugger
Name:           gdb
Version:        7.12.1
Release:        4%{?dist}
License:        GPLv2+
URL:            http://www.gnu.org/software/%{name}
Source0:        http://ftp.gnu.org/gnu/gdb/%{name}-%{version}.tar.xz
%define sha1    gdb=ef77c5345d6f9fdcdf7a5d8503301242b701936e
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Patch0:         gdb-7.12-pstack.patch
Requires:       expat
Requires:       ncurses
BuildRequires:  expat-devel
BuildRequires:  ncurses-devel
BuildRequires:  python3-devel
BuildRequires:  python3-libs
%if %{with_check}
BuildRequires:  dejagnu
%endif

%description
GDB, the GNU Project debugger, allows you to see what is going on 
`inside' another program while it executes -- or what 
another program was doing at the moment it crashed. 
%prep
%setup -q
%patch0 -p1

%build
./configure \
    --prefix=%{_prefix} \
    --with-python=/usr/bin/python3
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
rm %{buildroot}%{_infodir}/dir

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
%find_lang %{name} --all-name

%check
make %{?_smp_mflags} check

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

%changelog
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
