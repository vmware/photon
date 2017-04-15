Summary:	C debugger
Name:		gdb
Version:	7.12.1
Release:	1%{?dist}
License:	GPLv2+
URL:		http://www.gnu.org/software/%{name}
Source0:	http://ftp.gnu.org/gnu/gdb/%{name}-%{version}.tar.xz
%define sha1 gdb=ef77c5345d6f9fdcdf7a5d8503301242b701936e
Source1:        http://heanet.dl.sourceforge.net/sourceforge/tcl/tcl8.5.14-src.tar.gz
%define sha1 tcl=9bc452eec453c2ed37625874b9011563db687b07
Source2:        http://prdownloads.sourceforge.net/expect/expect5.45.tar.gz
%define sha1 expect=e634992cab35b7c6931e1f21fbb8f74d464bd496
Source3:         https://ftp.gnu.org/pub/gnu/dejagnu/dejagnu-1.5.3.tar.gz
%define sha1 dejagnu=d81288e7d7bd38e74b7fee8e570ebfa8c21508d9
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
Requires:	python2
Requires:	expat
Requires:	ncurses
BuildRequires:	expat-devel
BuildRequires:	ncurses-devel
BuildRequires:	python2-devel
BuildRequires:	python2-libs
%description
GDB, the GNU Project debugger, allows you to see what is going on 
`inside' another program while it executes -- or what 
another program was doing at the moment it crashed. 
%prep
%setup -q
tar xf %{SOURCE1} --no-same-owner
tar xf %{SOURCE2} --no-same-owner
tar xf %{SOURCE3} --no-same-owner

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
%find_lang %{name} --all-name

%check
pushd tcl8.5.14/unix
./configure --enable-threads --prefix=/usr
make
make install
popd

pushd expect5.45
./configure --prefix=/usr
make
make install
ln -svf expect5.45/libexpect5.45.so /usr/lib
popd

pushd dejagnu-1.5.3
./configure --prefix=/usr
make
make install 
popd

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
*   Wed Mar 22 2017 Alexey Makhalov <amakhalov@vmware.com> 7.12.1-1
-   Version update
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.8.2-3
-   GA - Bump release of all rpms
*   Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 7.8.2-2
-   Handled locale files with macro find_lang
*   Wed Apr 08 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.8.2-1
-   Initial build. First version
