Summary:        C debugger
Name:           gdb
Version:        7.8.2
Release:        5%{?dist}
License:        GPLv2+
URL:            http://www.gnu.org/software/%{name}
Source0:        http://ftp.gnu.org/gnu/gdb/%{name}-%{version}.tar.gz
%define sha1    gdb=67cfbc6efcff674aaac3af83d281cf9df0839ff9
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
Requires:       python3
Requires:       expat
Requires:       ncurses >= 6.0-3
BuildRequires:  expat
BuildRequires:  ncurses-devel >= 6.0-3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
%description
GDB, the GNU Project debugger, allows you to see what is going on 
`inside' another program while it executes -- or what 
another program was doing at the moment it crashed. 
%prep
%setup -q
%build
./configure \
    --prefix=%{_prefix}
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
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files -f %{name}.lang
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/gdb/*.h
%{_libdir}/*.so
%{_infodir}/*.gz
%{_datadir}/gdb/python/*
%{_datadir}/gdb/syscalls/*
%{_datadir}/gdb/system-gdbinit/*
%{_bindir}/*
%{_mandir}/*/*

%changelog
*   Tue May 30 2017 Xiaolin Li <xiaolinl@vmware.com> 7.8.2-5
-   Build gdb with python3.
*   Mon Apr 3 2017 Alexey Makhalov <amakhalov@vmware.com> 7.8.2-4
-   Use specified version of ncurses wich has long chtype and mmask_t
    (see ncurses changelog)
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.8.2-3
-   GA - Bump release of all rpms
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 7.8.2-2
-   Handled locale files with macro find_lang
*   Wed Apr 08 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.8.2-1
-   Initial build. First version
