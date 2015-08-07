%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\((VMS|Win32|BSD::|DB\\)$)
# unicore::Name - it's needed by perl, maybe problem of rpm
# FCGI is external dependency after install of perl-CGI, remove it during RC releases
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((VMS|BSD::|Win32|Tk|Mac::|Your::Module::Here|unicore::Name|FCGI)

Summary:	Practical Extraction and Report Language
Name:		perl
Version:	5.18.2
Release:	2%{?dist}
License:	GPLv1+
URL:		http://www.perl.org/
Group:		Development/Languages
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.cpan.org/src/5.0/%{name}-%{version}.tar.bz2
%define sha1 perl=b8b87ef46630b5a2287b86b6e0c69088da36adfd
Provides:	perl >= 0:5.003000
Provides:	perl(getopts.pl)
Provides:   /bin/perl
Requires:	zlib 
Requires:	gdbm
Requires:	glibc
Requires:	libgcc
%description
The Perl package contains the Practical Extraction and
Report Language.
%prep
%setup -q

sed -i 's/-fstack-protector/&-all/' Configure

sed -i -e "s|BUILD_ZLIB\s*= True|BUILD_ZLIB = False|" \
	-e "s|INCLUDE\s*= ./zlib-src|INCLUDE = /usr/include|" \
	-e "s|LIB\s*= ./zlib-src|LIB = /usr/lib|" \
	cpan/Compress-Raw-Zlib/config.in

%build
CFLAGS="%{_optflags}"

sh Configure -des \
	-Dprefix=%{_prefix} \
	-Dvendorprefix=%{_prefix} \
	-Dman1dir=%{_mandir}/man1 \
	-Dman3dir=%{_mandir}/man3 \
	-Dpager=%{_bindir}"/less -isR" \
	-Duseshrplib \
        -DPERL_RANDOM_DEVICE="/dev/erandom"

make VERBOSE=1 %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%{_bindir}/*
%dir %{_libdir}/perl5
%dir %{_libdir}/perl5/%{version}
%{_libdir}/perl5/%{version}/*
%{_mandir}/*/*
%changelog
*	Thu Jun 4 2015 Touseef Liaqat <tliaqat@vmware.com> 5.18.2-2
-	Provide /bin/perl.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 5.18.2-1
-	Initial build. First version
