# Got the intial spec from Fedora and modified it
Summary:	Provide the stuff missing in List::Util
Name:		perl-List-MoreUtils
Version:	0.410
Release:	1%{?dist}
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/List-MoreUtils/
Source0:	http://search.cpan.org/CPAN/authors/id/R/RE/REHSACK/List-MoreUtils-%{version}.tar.gz
%define sha1 List-MoreUtils=e72c962a78850f08212df5d9bd0b0b59b5a3caa4
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	perl
Requires:	perl
BuildRequires:	perl-Exporter-Tiny
Requires:	perl-Exporter-Tiny

%description
List::MoreUtils provides some trivial but commonly needed functionality
on lists that is not going to go into List::Util.

%prep
%setup -q -n List-MoreUtils-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}" NO_PERLLOCAL=1 NO_PACKLIST=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%{perl_vendorarch}/auto/List/
%{perl_vendorarch}/List/
%{_libdir}/perl5/*
%{_mandir}/man3/List::MoreUtils.3*
%{_mandir}/man3/List::MoreUtils::PP.3*
%{_mandir}/man3/List::MoreUtils::XS.3*

%changelog
*	Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 0.410-1
-	Initial version.
