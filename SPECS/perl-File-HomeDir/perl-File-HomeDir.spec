Summary:        File-HomeDir
Name:           perl-File-HomeDir
Version:        1.006
Release:        2%{?dist}
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/File-HomeDir/
Source0:        https://cpan.metacpan.org/authors/id/R/RE/REHSACK/File-HomeDir-%{version}.tar.gz
%define sha512  File-HomeDir=1ea90d68ed059ef5e890f6afb1280673dd5a597956f282c4ae8b4471c1751aa3cb2fcbe9caa6b2976937d11fd7233aa85a2dea611f87c79e0ddd1a501ceb890d

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl
%if 0%{?with_check}
BuildRequires:  perl-File-Which
%endif
Requires:       perl
Requires:       perl-File-Which

%description
File::HomeDir is a module for locating the directories that are "owned" by a user (typicaly your user) and to solve the various issues that arise trying to find them consistently across a wide variety of platforms.

%prep
%autosetup -n File-HomeDir-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
make %{?_smp_mflags} test

%files
%{perl_vendorlib}/File/HomeDir.pm
%{perl_vendorlib}/File/HomeDir/Darwin.pm
%{perl_vendorlib}/File/HomeDir/Darwin/Carbon.pm
%{perl_vendorlib}/File/HomeDir/Darwin/Cocoa.pm
%{perl_vendorlib}/File/HomeDir/Driver.pm
%{perl_vendorlib}/File/HomeDir/FreeDesktop.pm
%{perl_vendorlib}/File/HomeDir/MacOS9.pm
%{perl_vendorlib}/File/HomeDir/Test.pm
%{perl_vendorlib}/File/HomeDir/Unix.pm
%{perl_vendorlib}/File/HomeDir/Windows.pm
%{_mandir}/man3
%{_mandir}/man3/File::HomeDir.3.gz
%{_mandir}/man3/File::HomeDir::Darwin.3.gz
%{_mandir}/man3/File::HomeDir::Darwin::Carbon.3.gz
%{_mandir}/man3/File::HomeDir::Darwin::Cocoa.3.gz
%{_mandir}/man3/File::HomeDir::Driver.3.gz
%{_mandir}/man3/File::HomeDir::FreeDesktop.3.gz
%{_mandir}/man3/File::HomeDir::MacOS9.3.gz
%{_mandir}/man3/File::HomeDir::Test.3.gz
%{_mandir}/man3/File::HomeDir::Unix.3.gz
%{_mandir}/man3/File::HomeDir::Windows.3.gz

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.006-2
- Release bump for SRP compliance
* Thu Dec 08 2022 Gerrit Photon <photon-checkins@vmware.com> 1.006-1
- Automatic Version Bump
* Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 1.004-2
- Rebuilding for perl 5.30.1
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.004-1
- Update to version 1.004
* Tue Aug 08 2017 Chang Lee <changlee@vmware.com> 1.00-3
- Add perl-File-Which for make check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.00-2
- GA - Bump release of all rpms
* Thu Mar 3 2016 Xiaolin Li <xiaolinl@vmware.com> 1.00-1
- Initial version.
