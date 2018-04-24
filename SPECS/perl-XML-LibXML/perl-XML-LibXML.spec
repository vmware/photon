Summary:        Perl interface to the Gnome libxml2 library
Name:           perl-XML-LibXML
Version:        2.0132
Release:        1%{?dist}
Group:          Development/Libraries
License:        (GPL+ or Artistic) and Public Domain
URL:            http://search.cpan.org/dist/XML-LibXML/
Source0:        http://search.cpan.org/CPAN/authors/id/S/SH/SHLOMIF/XML-LibXML-%{version}.tar.gz
%define sha1    XML-LibXML=c5e316a5fabd656324d9d75c33b2593289c28c33
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  libxml2-devel >= 2.9.6
BuildRequires:  perl
BuildRequires:  perl-DBI
Requires:       perl-DBI
Requires:       perl
Requires:       perl-XML-NamespaceSupport
Requires:       perl-XML-SAX

%description
This module implements a Perl interface to the Gnome libxml2 library which
provides interfaces for parsing and manipulating XML files. This module allows
Perl programmers to make use of the highly capable validating XML parser and
the high performance DOM implementation.

%prep
%setup -q -n XML-LibXML-%{version}

%build
CFLAGS="%{optflags}" perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags} OPTIMIZE="%{optflags}"

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o \
     -name '*.bs' -size 0 \) -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

%check
make test

%files
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/XML/
%{_mandir}/man3/*

%changelog
*   Tue Apr 24 2018 Xiaolin Li <xiaolinl@vmware.com> 2.0132-1
-   Initial version.
