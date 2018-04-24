%global debug_package %{nil}
Summary:        Offers a simple way to process namespaced XML names
Name:           perl-XML-NamespaceSupport
Version:        1.12
Release:        1%{?dist}
Group:          Development/Libraries
License:        (GPL+ or Artistic) and Public Domain
URL:            http://search.cpan.org/dist/XML-NamespaceSupport/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PERIGRIN/XML-NamespaceSupport-%{version}.tar.gz
%define sha1    XML-NamespaceSupport=f07cf650e0bd52714fc3da39d19a95bc6290e4ef
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  perl
BuildRequires:  perl-DBI
Requires:       perl-DBI
Requires:       perl
BuildArch:      noarch

%description
This module offers a simple way to process namespaced XML names (unames) from within any application that may need them. It also helps maintain a prefix to namespace URI map, and provides a number of basic checks.

The model for this module is SAX2's NamespaceSupport class, readable at
http://www.saxproject.org/namespaces.html

%prep
%setup -q -n XML-NamespaceSupport-%{version}

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
*   Tue Apr 24 2018 Xiaolin Li <xiaolinl@vmware.com> 1.12-1
-   Initial version.
