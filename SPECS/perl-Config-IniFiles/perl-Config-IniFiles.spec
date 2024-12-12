# Got the intial spec from Fedora and modified it
Summary:        A module for reading .ini-style configuration files
Name:           perl-Config-IniFiles
Version:        3.000003
Release:        3%{?dist}
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Config-IniFiles/
Source0:        https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/Config-IniFiles-%{version}.tar.gz
%define sha512  Config-IniFiles=29278b7f6aaf9ffcc0cd8b48ca0e1f1084b10278e50764b2b93e3e9b156ef13d6e54f779f41d0a6cbf6e0b23da1b73a3bb83fbf873add0a604693a41312b91f5

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl
Requires:       perl
BuildRequires:  perl-List-MoreUtils
BuildRequires:  perl-Module-Build
Requires:       perl-List-MoreUtils

%description
Config::IniFiles provides a way to have readable configuration files
outside your Perl script. Configurations can be imported (inherited,
stacked,...), sections can be grouped, and settings can be accessed
from a tied hash.

%prep
%autosetup -n Config-IniFiles-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make %{?_smp_mflags} pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w %{buildroot}/*

%check
# Upstream: make test fails in chrooted environment at -
#   - t/34trailing-comments-double-delimeter.t
#   - t/35section-iterators.t
if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
rm t/34trailing-comments-double-delimeter.t t/35section-iterators.t
fi
make %{?_smp_mflags} test

%files
%{perl_vendorlib}/Config/
%{_mandir}/man3/*

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 3.000003-3
- Release bump for SRP compliance
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 3.000003-2
- Perl version upgrade to 5.36.0
* Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 3.000003-1
- Automatic Version Bump
* Mon Dec 03 2018 Dweep Advani <dadvani@vmware.com> 3.000000-2
- Fix makecheck tests
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 3.000000-1
- Update to version 3.000000
* Tue Aug 8 2017 Chang Lee <changlee@vmware.com> 2.94-2
- Remove 34trailing-comments-double-delimeter test in a chrooted environment
* Mon Apr 3 2017 Robert Qi <qij@vmware.com> 2.94-1
- Updated to 2.94
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.88-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 2.88-1
- Updated to version 2.88
* Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 2.83-2
- Add build requirement
* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 2.83-1
- Initial version.
