# Got the intial spec from Fedora and modified it
Summary:        A module for reading .ini-style configuration files
Name:           perl-Config-IniFiles
Version:        2.94
Release:        1%{?dist}
Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/Config-IniFiles/
Source0:        http://www.cpan.org/authors/id/S/SH/SHLOMIF/Config-IniFiles-%{version}.tar.gz
%define sha1 Config-IniFiles=df7e1a9244dd60623ffc004e9302daabb46e35d0
Vendor:		VMware, Inc.
Distribution:	Photon
BuildArch:      noarch
BuildRequires:	perl
Requires:	perl
BuildRequires:	perl-List-MoreUtils
BuildRequires:	perl-Module-Build
Requires:	perl-List-MoreUtils

%description
Config::IniFiles provides a way to have readable configuration files
outside your Perl script. Configurations can be imported (inherited,
stacked,...), sections can be grouped, and settings can be accessed
from a tied hash.

%prep
%setup -q -n Config-IniFiles-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check
make test

%files
%{perl_vendorlib}/Config/
%{_mandir}/man3/*

%changelog
*   Mon Apr 3 2017 Robert Qi <qij@vmware.com> 2.94-1
-   Updated to 2.94
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.88-2
-	GA - Bump release of all rpms
*   Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 2.88-1
-   Updated to version 2.88
*	Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 2.83-2
-	Add build requirement
*	Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 2.83-1
-	Initial version.
