%global build_if %{photon_subrelease} >= 91

Summary:        Cross-platform path specification manipulation for Perl
Name:           perl-Path-Class
Version:        0.37
Release:        8%{?dist}
URL:            http://search.cpan.org/~kwilliams/Path-Class-0.37/
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://search.cpan.org/CPAN/authors/id/K/KW/KWILLIAMS/Path-Class-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildArch:      noarch
Requires:       perl >= 5.42.2
BuildRequires:  perl >= 5.42.2

%description
Path::Class is a module for manipulation of file and directory specifications (strings describing their locations, like '/home/ken/foo.txt' or 'C:\Windows\Foo.txt') in a cross-platform manner. It supports pretty much every platform Perl runs on, including Unix, Windows, Mac, VMS, Epoc, Cygwin, OS/2, and NetWare.

The well-known module File::Spec also provides this service, but it's sort of awkward to use well, so people sometimes avoid it, or use it in a way that won't actually work properly on platforms significantly different than the ones they've tested their code on.

%prep
%autosetup -n Path-Class-%{version}
%if 0%{?with_check} == 0
  rm -rf Changes INSTALL t/
%endif

%build
env PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
make %{?_smp_mflags} test

%files
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
* Thu Apr 16 2026 Dweep Advani <dweep.advani@broadcom.com> 0.37-8
- Release bump for perl 5.42.2 upgrade
* Wed Jun 11 2025 Dweep Advani <dweep.advani@broadcom.com> 0.37-7
- Release bump for perl 5.40.2 upgrade
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 0.37-6
- Release bump for SRP compliance
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 0.37-5
- Perl version upgrade to 5.36.0
* Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 0.37-4
- Rebuilding for perl 5.30.1
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 0.37-3
- Consuming perl version upgrade of 5.28.0
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.37-2
- Fix arch
* Wed Apr 19 2017 Xiaolin Li <xiaolinl@vmware.com> 0.37-1
- Initial version.
