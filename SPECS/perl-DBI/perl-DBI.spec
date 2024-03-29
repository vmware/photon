# Got the intial spec from Fedora and modified it
# Filter unwanted dependencies
%global __requires_exclude %{?__requires_exclude|%__requires_exclude|}^perl\\(RPC::\\)

%define perl_vendorarchdir %(test %{_host} == %{_build} && echo %{perl_vendorarch} || echo %{perl_vendorarch} | sed 's/x86_64-linux-thread-multi/%{_arch}-linux/')

# According to documentation, module using Coro is just:
# A PROOF-OF-CONCEPT IMPLEMENTATION FOR EXPERIMENTATION.
# Omit Coro support on bootsrap bacause perl-DBI is pulled in by core
# perl-CPANPLUS.
%bcond_without coro

Summary:        A database access API for perl
Name:           perl-DBI
Version:        1.643
Release:        2%{?dist}
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://dbi.perl.org/
# The source tarball must be repackaged to remove the DBI/FAQ.pm, since the
# license is not a FSF free license.
Source0:        https://cpan.metacpan.org/authors/id/T/TI/TIMB/DBI-%{version}.tar.gz
%define sha512  DBI=03812f3eb1e43c8290dadb8cb14bbced9ec6e237228ea2a2ba91f22e52143906a91a7e82945dab30b1d1b9fc925073721111adafd9a09fac070808ab88f908b8
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  perl
Requires:       perl

%description
DBI is a database access Application Programming Interface (API) for
the Perl Language. The DBI API Specification defines a set of
functions, variables and conventions that provide a consistent
database interface independent of the actual database being used.

%prep
%autosetup -n DBI-%{version}
for F in lib/DBD/Gofer.pm; do
    iconv -f ISO-8859-1 -t UTF-8 < "$F" > "${F}.utf8"
    touch -r "$F" "${F}.utf8"
    mv "${F}.utf8" "$F"
done
chmod 644 ex/*
chmod 744 dbixs_rev.pl
# Fix shell bangs
for F in dbixs_rev.pl ex/corogofer.pl; do
    perl -MExtUtils::MakeMaker -e "ExtUtils::MM_Unix->fixin(q{$F})"
done

rm lib/DBD/Gofer/Transport/corostream.pm
sed -i -e '/^lib\/DBD\/Gofer\/Transport\/corostream.pm$/d' MANIFEST

# Remove RPC::Pl* reverse dependencies due to security concerns,
# CVE-2013-7284, bug #1051110
for F in lib/Bundle/DBI.pm lib/DBD/Proxy.pm lib/DBI/ProxyServer.pm \
        dbiproxy.PL t/80proxy.t; do
    rm "$F"
    sed -i -e '\|^'"$F"'|d' MANIFEST
done
sed -i -e 's/"dbiproxy$ext_pl",//' Makefile.PL
# Remove Win32 specific files to avoid unwanted dependencies
for F in lib/DBI/W32ODBC.pm lib/Win32/DBIODBC.pm; do
    rm "$F"
    sed -i -e '\|^'"$F"'|d' MANIFEST
done

%build
perl Makefile.PL INSTALLDIRS=vendor AR=%{_host}-ar CC=%{_host}-gcc LD=%{_host}-gcc OPTIMIZE="%{optflags}"
if [ %{_host} != %{_build} ]; then
sed -i 's/x86_64-linux-thread-multi/%{_arch}-linux/' Makefile
sed -i 's/PERL_ARCHLIBDEP = /PERL_ARCHLIBDEP = \/target-%{_arch}/' Makefile
sed -i 's/PERL_INC = /PERL_INC = \/target-%{_arch}/' Makefile
sed -i 's/PERL_INCDEP = /PERL_INCDEP = \/target-%{_arch}/' Makefile
sed -i 's/-L\/usr\/local\/lib//' Makefile
fi
make %{?_smp_mflags}

%install
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} '%{buildroot}'/*

%check
make %{?_smp_mflags} test

%files
%{_bindir}/dbipro*
%{_bindir}/dbilogstrip
%{perl_vendorarchdir}/*.p*
%{perl_vendorarchdir}/DBD/
%{perl_vendorarchdir}/DBI/
%{perl_vendorarchdir}/auto/DBI/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
*   Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 1.643-2
-   Perl version uprade to 5.36.0
*   Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 1.643-1
-   Automatic Version Bump
*   Fri Nov 09 2018 Alexey Makhalov <amakhalov@vmware.com> 1.641-2
-   Cross compilation support
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.641-1
-   Update to version 1.641
*   Mon Apr 3 2017 Robert Qi <qij@vmware.com> 1.636-1
-   Upgraded to 1.636
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.634-2
-   GA - Bump release of all rpms
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.634-1
-   Upgrade version
*   Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.633-1
-   Initial version.
