# Got the intial spec from Fedora and modified it
Summary:	Internationalization library for Perl, compatible with gettext
Name:		perl-libintl
Version:	1.23
Release:	1%{?dist}
License:	LGPLv2+
Group: 		Development/Libraries
URL: 		http://search.cpan.org/dist/libintl-perl/
Source: 	http://search.cpan.org/CPAN/authors/id/G/GU/GUIDO/libintl-perl-%{version}.tar.gz
%define sha1 libintl-perl=da2ed849f3b3f28dc5306a2887126a55f49992cb
Vendor:		VMware, Inc.
Distribution:	Photon
Requires: 	perl
Provides: 	perl-libintl-perl = %{version}-%{release}
BuildRequires: 	perl

%description
The package libintl-perl is an internationalization library for Perl that
aims to be compatible with the Uniforum message translations system as
implemented for example in GNU gettext.


%prep
%setup -q -n libintl-perl-%{version}
find -type f -exec chmod -x {} \;
find lib/Locale gettext_xs \( -name '*.pm' -o -name '*.pod' \) \
    -exec sed -i -e '/^#! \/bin\/false/d' {} \;

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o \
			-name '*.bs' -size 0 \) -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*

%check
make test

%files
%{perl_vendorlib}/Locale/
%{perl_vendorarch}/auto/Locale/
%{_mandir}/man?/*

%changelog
*	Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.23-1
-	Initial version.

