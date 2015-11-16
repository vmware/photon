Summary:	The GNU Database Manager
Name:		gdbm
Version:	1.11
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/gdbm
Group:		Applications/Databases
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://ftp.gnu.org/gnu/gdbm/%{name}-%{version}.tar.gz
%define sha1 gdbm=ce433d0f192c21d41089458ca5c8294efe9806b4
%description
This is a disk file format database which stores key/data-pairs in
single files. The actual data of any record being stored is indexed
by a unique key, which can be retrieved in less time than if it was
stored in a text file.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--enable-libgdbm-compat \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}
%find_lang %{name}
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*
%{_mandir}/*/*
%changelog
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.11-1
-	Initial build.	First version
