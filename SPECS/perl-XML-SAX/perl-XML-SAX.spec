%global debug_package %{nil}
Summary:        Simple API for XML
Name:           perl-XML-SAX
Version:        1.00
Release:        1%{?dist}
Group:          Development/Libraries
License:        (GPL+ or Artistic) and Public Domain
URL:            http://search.cpan.org/dist/XML-SAX/
Source0:        http://search.cpan.org/CPAN/authors/id/G/GR/GRANTM/XML-SAX-%{version}.tar.gz
%define sha1    XML-SAX=1151e38f305dd1362372c6f9834fae2200d90dbc
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  perl
BuildRequires:  perl-DBI
Requires:       perl-DBI
Requires:       perl
Requires:       perl-XML-NamespaceSupport
BuildArch:      noarch

%description
XML::SAX is a SAX parser access API for Perl. It includes classes and APIs required for implementing SAX drivers, along with a factory class for returning any SAX parser installed on the user's system.

%prep
%setup -q -n XML-SAX-%{version}

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
%{perl_vendorlib}/XML/*
%{_mandir}/man3/*

%changelog
*   Tue Apr 24 2018 Xiaolin Li <xiaolinl@vmware.com> 1.00-1
-   Initial version.
