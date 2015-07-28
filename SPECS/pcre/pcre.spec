Summary:	Grep for perl compatible regular expressions
Name:		pcre
Version:	8.36
Release:	1%{?dist}
License:	BSD
URL:		ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.36.tar.gz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{name}-%{version}.tar.gz
%define sha1 pcre=fb537757756818133d8157ec878bc11f5a93ef4d
BuildRequires:	bzip2-devel
BuildRequires:	readline-devel
Requires:       libgcc
Requires:       libstdc++
%description
The PCRE package contains Perl Compatible Regular Expression libraries. These are useful for implementing regular expression pattern matching using the same syntax and semantics as Perl 5.

%package 	devel
Group:          Development/Libraries
Summary:        Headers and static lib for pcre development
Requires:	%{name} = %{version}
Provides:	pkgconfig(libpcre)
%description 	devel
Install this package if you want do compile applications using the pcre
library.

%prep
%setup -q
%build
./configure --prefix=/usr                     \
            --docdir=/usr/share/doc/pcre-8.36 \
            --enable-unicode-properties       \
            --enable-pcre16                   \
            --enable-pcre32                   \
            --enable-pcregrep-libz            \
            --enable-pcregrep-libbz2          \
            --enable-pcretest-libreadline     \
            --disable-static
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
mv -v %{buildroot}/usr/lib/libpcre.so.* %{buildroot}/lib &&
ln -sfv ../../lib/$(readlink %{buildroot}/usr/lib/libpcre.so) %{buildroot}/usr/lib/libpcre.so
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_bindir}/pcregrep  
%{_bindir}/pcretest
%{_mandir}/man1/pcregrep.1*
%{_mandir}/man1/pcretest.1*
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_bindir}/*
%exclude %{_bindir}/pcregrep  
%exclude %{_bindir}/pcretest
%{_defaultdocdir}/%{name}-%{version}/*
%{_mandir}/*/*
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%changelog
*	Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 8.36
	Initial version
