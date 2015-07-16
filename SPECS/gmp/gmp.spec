Summary:	Math libraries
Name:		gmp
Version:	5.1.3
Release:	1%{?dist}
License:	LGPLv3+
URL:		http://www.gnu.org/software/gmp
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnu.org/gnu/gmp/%{name}-%{version}.tar.xz
%define sha1 gmp=12cfe0911d64fcbd85835df9ddc18c99af8f9a45
%description
The GMP package contains math libraries. These have useful functions
for arbitrary precision arithmetic.
%package	devel
Summary:	Header and development files for gmp
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications 
for handling compiled objects.
%prep
%setup -q
%build
%ifarch i386 i486 i586 i686
	ABI=32 ./configure \
	--prefix=%{_prefix} \
	--enable-cxx \
	--disable-silent-rules
%else
	./configure \
	--prefix=%{_prefix} \
	--enable-cxx \
	--disable-silent-rules
%endif
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm 755 %{buildroot}%{_defaultdocdir}/%{name}-%{version}
cp    -v doc/{isa_abi_headache,configuration} doc/*.html %{buildroot}%{_defaultdocdir}/%{name}-%{version}
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_libdir}/libgmp.so.10
%{_libdir}/libgmpxx.so.4.3.3
%{_libdir}/libgmp.so.10.1.3
%{_libdir}/libgmpxx.so.4
%{_docdir}/gmp-5.1.3/tasks.html
%{_docdir}/gmp-5.1.3/projects.html
%{_docdir}/gmp-5.1.3/configuration
%{_docdir}/gmp-5.1.3/isa_abi_headache
%files devel
%{_includedir}/gmpxx.h
%{_includedir}/gmp.h
%{_libdir}/libgmp.a
%{_libdir}/libgmpxx.a
%{_libdir}/libgmpxx.so
%{_libdir}/libgmp.so
%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.1.3-1
-	Initial build. First version
