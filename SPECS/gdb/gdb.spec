Summary:	C debugger
Name:		gdb
Version:	7.8.2	
Release:	1%{?dist}
License:	GPLv2+
URL:		http://www.gnu.org/software/%{name}
Source0:	http://ftp.gnu.org/gnu/gdb/%{name}-%{version}.tar.gz
%define sha1 gdb=67cfbc6efcff674aaac3af83d281cf9df0839ff9
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
Requires:	python2
Requires:	expat
Requires:	ncurses
BuildRequires:	expat
BuildRequires:	ncurses-devel
BuildRequires:	python2-devel
BuildRequires:	python2-libs
%description
GDB, the GNU Project debugger, allows you to see what is going on 
`inside' another program while it executes -- or what 
another program was doing at the moment it crashed. 
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix}
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
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
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
%lang(da) %{_datarootdir}/locale/da/LC_MESSAGES/bfd.mo
%lang(da) %{_datarootdir}/locale/da/LC_MESSAGES/opcodes.mo
%lang(es) %{_datarootdir}/locale/es/LC_MESSAGES/bfd.mo
%lang(es) %{_datarootdir}/locale/es/LC_MESSAGES/opcodes.mo
%lang(fr) %{_datarootdir}/locale/fr/LC_MESSAGES/bfd.mo
%lang(fr) %{_datarootdir}/locale/fr/LC_MESSAGES/opcodes.mo
%lang(ga) %{_datarootdir}/locale/ga/LC_MESSAGES/opcodes.mo
%lang(id) %{_datarootdir}/locale/id/LC_MESSAGES/bfd.mo
%lang(id) %{_datarootdir}/locale/id/LC_MESSAGES/opcodes.mo
%lang(it) %{_datarootdir}/locale/it/LC_MESSAGES/opcodes.mo
%lang(ja) %{_datarootdir}/locale/ja/LC_MESSAGES/bfd.mo
%lang(nl) %{_datarootdir}/locale/nl/LC_MESSAGES/opcodes.mo
%lang(pt_BR) %{_datarootdir}/locale/pt_BR/LC_MESSAGES/opcodes.mo
%lang(ro) %{_datarootdir}/locale/ro/LC_MESSAGES/bfd.mo
%lang(ro) %{_datarootdir}/locale/ro/LC_MESSAGES/opcodes.mo
%lang(ru) %{_datarootdir}/locale/ru/LC_MESSAGES/bfd.mo
%lang(rw) %{_datarootdir}/locale/rw/LC_MESSAGES/bfd.mo
%lang(sv) %{_datarootdir}/locale/sv/LC_MESSAGES/bfd.mo
%lang(sv) %{_datarootdir}/locale/sv/LC_MESSAGES/opcodes.mo
%lang(tr) %{_datarootdir}/locale/tr/LC_MESSAGES/bfd.mo
%lang(tr) %{_datarootdir}/locale/tr/LC_MESSAGES/opcodes.mo
%lang(uk) %{_datarootdir}/locale/uk/LC_MESSAGES/bfd.mo
%lang(uk) %{_datarootdir}/locale/uk/LC_MESSAGES/opcodes.mo
%lang(vi) %{_datarootdir}/locale/vi/LC_MESSAGES/bfd.mo
%lang(vi) %{_datarootdir}/locale/vi/LC_MESSAGES/opcodes.mo
%lang(zh_CN) %{_datarootdir}/locale/zh_CN/LC_MESSAGES/bfd.mo
%lang(zh_CN) %{_datarootdir}/locale/zh_CN/LC_MESSAGES/opcodes.mo
%changelog
*	Wed Apr 08 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.8.2-1
-	Initial build. First version
