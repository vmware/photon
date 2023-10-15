Name:           perl-Clone
Version:        0.46
Release:        1%{?dist}
Summary:        Recursively copy perl data types
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Clone
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://cpan.metacpan.org/modules/by-module/Clone/Clone-%{version}.tar.gz
%define sha512 Clone=f8bb1010364e94c7cc8bba25681cd9fd737ec2935a8be960ac53099359729fc679190a115dd082fccd239b35762dee2b3be3adbddce37e4ceae6fe934fbad545

BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  perl

%description
This module provides a clone() method that makes recursive
copies of nested hash, array, scalar and reference types,
including tied variables and objects.

clone() takes a scalar argument and an optional parameter that
can be used to limit the depth of the copy. To duplicate lists,
arrays or hashes, pass them in by reference.

%prep
%autosetup -p1 -n Clone-%{version}

%build
perl Makefile.PL NO_PACKLIST=1 INSTALLDIRS=vendor NO_PERLLOCAL=1
%make_build

%install
%make_install %{?_smp_mflags} pure_install
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete
%{_fixperms} -c %{buildroot}

%check
%make_build test

%files
%doc Changes README.md
%{perl_vendorarch}/auto/Clone/
%{perl_vendorarch}/Clone.pm
%{_mandir}/man3/Clone.3*

%changelog
* Sun Oct 15 2023 Shreenidhi Shedi <sshedi@vmware.com> 0.46-1
- Intial version. Needed by perl-Crypt-SSLeay.
