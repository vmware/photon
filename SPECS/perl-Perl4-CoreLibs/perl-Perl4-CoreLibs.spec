%define cpan_name Perl4-CoreLibs
Summary:        Core Perl4 Libs
Name:           perl-Perl4-CoreLibs
Version:        0.004
Release:        2%{?dist}
License:        GPL-1.0+ or Artistic
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            http://search.cpan.org/dist/Perl4-CoreLibs/
Source0:        https://cpan.metacpan.org/authors/id/Z/ZE/ZEFRAM/%{cpan_name}-%{version}.tar.gz
%define sha1    %{cpan_name}=2f510e41e5c216f1379e35d808de9d5151e49331
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl-Module-Build
Requires:       perl
Provides:       perl(abbrev.pl)
Provides:       perl(assert.pl)
Provides:       perl(bigfloat.pl)
Provides:       perl(bigint.pl)
Provides:       perl(bigrat.pl)
Provides:       perl(cacheout.pl)
Provides:       perl(chat2.pl)
Provides:       perl(complete.pl)
Provides:       perl(ctime.pl)
Provides:       perl(dotsh.pl)
Provides:       perl(exceptions.pl)
Provides:       perl(fastcwd.pl)
Provides:       perl(find.pl)
Provides:       perl(finddepth.pl)
Provides:       perl(flush.pl)
Provides:       perl(ftp.pl)
Provides:       perl(getcwd.pl)
Provides:       perl(getopt.pl)
Provides:       perl(getopts.pl)
Provides:       perl(hostname.pl)
Provides:       perl(importenv.pl)
Provides:       perl(look.pl)
Provides:       perl(newgetopt.pl)
Provides:       perl(open2.pl)
Provides:       perl(open3.pl)
Provides:       perl(pwd.pl)
Provides:       perl(shellwords.pl)
Provides:       perl(stat.pl)
Provides:       perl(syslog.pl)
Provides:       perl(tainted.pl)
Provides:       perl(termcap.pl)
Provides:       perl(timelocal.pl)
Provides:       perl(validate.pl)

%description
This is a collection of '.pl' files that were bundled with the Perl core
until core version 5.15.1. Relying on their presence in the core
distribution is deprecated; they should be acquired from this CPAN
distribution instead. From core version 5.13.3 until their removal, the
core versions of these libraries emit a deprecation warning when loaded.
The CPAN version does not emit such a warning.

%prep
%setup -q -n %{cpan_name}-%{version}

%build
perl Build.PL installdirs=vendor
./Build build flags=%{?_smp_mflags}

%check
./Build test

%install
./Build install destdir=%{buildroot} create_packlist=0

%files
%{perl_vendorlib}
%{_mandir}/man3/*

%changelog
*   Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 0.004-2
-   Rebuilding for perl 5.30.1
*   Sat Oct 26 2019 Ankit Jain <ankitja@vmware.com> 0.004-1
-   initial version
