Summary:        Perl extension for generating and using LALR parsers
Name:           perl-Parse-Yapp
Version:        1.21
Release:        1%{?dist}
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Parse-Yapp
Group:          Development/Libraries/Perl
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://www.cpan.org/authors/id/W/WB/WBRASWELL/Parse-Yapp-%{version}.tar.gz
%define sha1 Parse-Yapp=dad25e0e73a4873ef021308b23d51bb2ccdc7ce4

BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl

Requires:       perl

%description
Parse::Yapp (Yet Another Perl Parser compiler) is a collection of modules that
let you generate and use yacc like thread safe (reentrant) parsers with perl
object oriented interface.  The script yapp is a front-end to the Parse::Yapp
module and let you easily create a Perl OO parser from an input grammar file.

%prep
%setup -q -n Parse-Yapp-%{version}
chmod 644 README lib/Parse/{*.pm,Yapp/*.pm}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot} %{?_smp_mflags}
chmod -R u+w %{buildroot}/*

%check
make test %{?_smp_mflags}

%files
%defattr(-,root,root,-)
%doc Changes README
%{_bindir}/yapp
%{perl_vendorlib}/Parse/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*


%changelog
*   Fri Mar 13 2020 Shreyas B. <shreyasb@vmware.com> 1.21-1
-   Initial version.
