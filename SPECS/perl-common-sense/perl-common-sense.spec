# Got the intial spec from Fedora and modified it
# This arch-specific package has no binaries and generates no debuginfo
%global debug_package %{nil}

Summary:	"Common sense" Perl defaults 
Name:		perl-common-sense
Version:	3.73
Release:	1%{?dist}
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/common-sense
Source0:	http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/common-sense-%{version}.tar.gz
%define sha1 common-sense=114bab46ac459f399ec3c7b2ae6a0d3b42d05c7c
Vendor:		VMware, Inc.
Distribution:	Photon 
BuildRequires:	perl
Requires:	perl
Patch1:		common-sense-3.71-podenc.patch

%description
This module implements some sane defaults for Perl programs, as defined
by two typical (or not so typical - use your common sense) specimens of
Perl coders:

It's supposed to be mostly the same, with much lower memory usage, as:
 
	use utf8;
	use strict qw(vars subs);
	use feature qw(say state switch);
	use feature qw(unicode_strings unicode_eval current_sub fc evalbytes);
	no feature qw(array_base);
	no warnings;
	use warnings qw(FATAL closed threads internal debugging pack
			portable prototype inplace io pipe unpack malloc
			deprecated glob digit printf layer
			reserved taint closure semicolon);
	no warnings qw(exec newline unopened);

%prep
%setup -q -n common-sense-%{version}

# Specify POD encoding
%patch1

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

# Have a non-empty manpage too
pod2man sense.pod > %{buildroot}%{_mandir}/man3/common::sense.3pm

%check
make test

%clean
rm -rf %{buildroot}

%files
%dir %{perl_vendorarch}/common/
%{perl_vendorarch}/common/sense.pm
%doc %{perl_vendorarch}/common/sense.pod
%{_mandir}/man3/common::sense.3*

%changelog
*	Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 3.73-1
-	Initial version.

