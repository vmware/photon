Summary:         Math libraries
Name:            gmp
Version:         6.1.2
Release:         1%{?dist}
License:         LGPLv3+
URL:             http://www.gnu.org/software/gmp
Group:           Applications/System
Vendor:          VMware, Inc.
Distribution:    Photon
Source0:         http://ftp.gnu.org/gnu/gmp/%{name}-%{version}.tar.xz
%define sha1 gmp=9dc6981197a7d92f339192eea974f5eca48fcffe

%description
The GMP package contains math libraries. These have useful functions
for arbitrary precision arithmetic.

%package    devel
Summary:    Header and development files for gmp
Requires:   %{name} = %{version}

%description    devel
It contains the libraries and header files to create applications
for handling compiled objects.

%prep
%setup -q -n %{name}-%{version}

%build
%ifarch i386 i486 i586 i686
    ABI=32 ./configure \
    --prefix=%{_prefix} \
    --enable-cxx \
    --disable-silent-rules \
    --disable-assembly
%else
    ./configure \
    --prefix=%{_prefix} \
    --enable-cxx \
    --disable-silent-rules \
    --disable-assembly
%endif
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp -v doc/{isa_abi_headache,configuration} doc/*.html %{buildroot}%{_defaultdocdir}/%{name}-%{version}
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/libgmp.so.10
%{_libdir}/libgmpxx.so.4.5.2
%{_libdir}/libgmp.so.10.3.2
%{_libdir}/libgmpxx.so.4
%{_docdir}/%{name}-%{version}/tasks.html
%{_docdir}/%{name}-%{version}/projects.html
%{_docdir}/%{name}-%{version}/configuration
%{_docdir}/%{name}-%{version}/isa_abi_headache

%files devel
%{_includedir}/gmpxx.h
%{_includedir}/gmp.h
%{_libdir}/libgmp.a
%{_libdir}/libgmpxx.a
%{_libdir}/libgmpxx.so
%{_libdir}/libgmp.so

%changelog
*	Mon Apr 17 2017 Danut Moraru <dmoraru@vmware.com> 6.1.2-1
-	Update to 6.1.2
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 6.0.0a-3
-	GA - Bump release of all rpms
*    Thu Apr 14 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 6.0.0a-2
-    Disable assembly and use generic C code
*    Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 6.0.0a-1
-    Updated to version 6.0.0
*    Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.1.3-1
-    Initial build. First version
