Summary:	The GNU Database Manager
Name:		gdbm
Version:	1.11
Release:	2%{?dist}
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

%package devel
Summary: Development libraries and header files for the gdbm library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Gdbm-devel contains the development libraries and header files for
gdbm, the GNU database system.  These libraries and header files are
necessary if you plan to do development using the gdbm database.

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
%{_mandir}/*/*

%files devel
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
*   Wed Oct 14 2015 Xiaolin Li <xiaolinl@vmware.com> 1.11-2
-   Move development libraries and header files to devel package.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.11-1
-	Initial build.	First version
