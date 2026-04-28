%global build_if %{photon_subrelease} >= 91

Summary:        File::ShareDir - Locate per-dist and per-module shared files
Name:           perl-File-ShareDir
Version:        1.118
Release:        1%{?dist}
Group:          Development/Libraries
URL:            https://metacpan.org/pod/File::ShareDir
Source0:        https://cpan.metacpan.org/authors/id/R/RE/REHSACK/File-ShareDir-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

Patch0:         perl-File-ShareDir-fix-Makefile.patch
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl >= 5.42.2
BuildRequires:  perl-Class-Inspector
BuildRequires:  perl-File-ShareDir-Install
Requires:       perl >= 5.42.2
Requires:       perl-Class-Inspector

%description
The File::ShareDir provides a companion to Class::Inspector and File::HomeDir
modules to make easy to have access to a large amount of read-only data that
is stored on the file-system at run-time.

%prep
%autosetup -n File-ShareDir-%{version}
%if 0%{?with_check} == 0
  rm -rf Changes inc/inc_File-ShareDir-Install/ share/sample.txt \
         share/subdir/sample.txt testrules.yml t/
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
make %{?_smp_mflags} test

%files
%{perl_vendorlib}/*
%{_mandir}/man3/File::ShareDir.3.gz

%changelog
* Thu Apr 30 2026 Dweep Advani <dweep.advani@broadcom.com> 1.118-1
- Introduce File::ShareDir needed at runtime by XML-Parser 2.57
