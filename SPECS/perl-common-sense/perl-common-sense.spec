# Got the intial spec from Fedora and modified it
# This arch-specific package has no binaries and generates no debuginfo
%global debug_package %{nil}

Summary:       "Common sense" Perl defaults
Name:          perl-common-sense
Version:       3.75
Release:       3%{?dist}
Group:         Development/Libraries
URL:           http://search.cpan.org/dist/common-sense
Source0:       http://search.cpan.org/CPAN/authors/id/M/ML/MLEHMANN/common-sense-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:        VMware, Inc.
Distribution:  Photon
BuildRequires: perl
Requires:      perl
Patch1:        common-sense-3.71-podenc.patch

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
%autosetup -n common-sense-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

# Have a non-empty manpage too
pod2man sense.pod > %{buildroot}%{_mandir}/man3/common::sense.3pm

%check
make %{?_smp_mflags} test

%clean
rm -rf %{buildroot}

%files
%dir %{perl_vendorarch}/common/
%{perl_vendorarch}/common/sense.pm
%doc %{perl_vendorarch}/common/sense.pod
%{_mandir}/man3/common::sense.3*

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 3.75-3
- Release bump for SRP compliance
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 3.75-2
- Perl version upgrade to 5.36.0
* Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 3.75-1
- Automatic Version Bump
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 3.74-3
- Consuming perl version upgrade of 5.28.0
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.74-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.74-1
- Upgraded to version 3.74
* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 3.73-1
- Initial version.
