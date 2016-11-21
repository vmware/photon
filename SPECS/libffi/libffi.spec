Summary:	A portable, high level programming interface to various calling conventions
Name:		libffi
Version:	3.2.1
Release:	3%{?dist}
License:	BSD
URL:		http://sourceware.org/libffi/
Group:		System Environment/GeneralLibraries
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	ftp://sourceware.org/pub/libffi/%{name}-%{version}.tar.gz
%define sha1 libffi=280c265b789e041c02e5c97815793dfc283fb1e6
Source1:        https://ftp.gnu.org/pub/gnu/dejagnu/dejagnu-1.5.3.tar.gz
%define sha1 dejagnu=d81288e7d7bd38e74b7fee8e570ebfa8c21508d9
Source2:        http://prdownloads.sourceforge.net/expect/expect5.45.tar.gz
%define sha1 expect=e634992cab35b7c6931e1f21fbb8f74d464bd496
Source3:        http://heanet.dl.sourceforge.net/sourceforge/tcl/tcl8.5.14-src.tar.gz
%define sha1 tcl=9bc452eec453c2ed37625874b9011563db687b07
Provides:	pkgconfig(libffi)
%description
The libffi library provides a portable, high level programming interface
to various calling conventions. This allows a programmer to call any 
function specified by a call interface description at run time.
%prep
%setup -q
tar xf %{SOURCE1} --no-same-owner
tar xf %{SOURCE2} --no-same-owner
tar xf %{SOURCE3} --no-same-owner
%build
sed -e '/^includesdir/ s:$(libdir)/@PACKAGE_NAME@-@PACKAGE_VERSION@/include:$(includedir):' \
    -i include/Makefile.in &&
sed -e '/^includedir/ s:${libdir}/@PACKAGE_NAME@-@PACKAGE_VERSION@/include:@includedir@:' \
    -e 's/^Cflags: -I${includedir}/Cflags:/' \
    -i libffi.pc.in        &&
./configure \
	CFLAGS="%{optflags}" \
	CXXFLAGS="%{optflags}" \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--libdir=%{_libdir} \
	--disable-static
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
%ifarch x86_64
find %{buildroot}/%{_lib64dir} -name '*.la' -delete
%else
find %{buildroot}/%{_libdir} -name '*.la' -delete
%endif
rm -rf %{buildroot}/%{_infodir}
%{_fixperms} %{buildroot}/*
%check
pushd tcl8.5.14/unix
./configure --enable-threads --prefix=/usr
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
make install
popd

make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
%ifarch x86_64
%{_lib64dir}/*.so*
%else
%{_libdir}/*.so*
%endif
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datarootdir}/licenses/libffi/LICENSE
%{_mandir}/man3/*
%changelog
*       Thu Oct 06 2016 ChangLee <changlee@vmware.com> 3.2.1-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2.1-2
-	GA - Bump release of all rpms
* 	Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 3.2.1-1
- 	Updated to version 3.2.1
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.1-1
-	Initial build.	First version
