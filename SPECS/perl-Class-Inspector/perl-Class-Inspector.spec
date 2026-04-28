%global build_if %{photon_subrelease} >= 91

Summary:        Class::Inspector - Get information about a class and its structure
Name:           perl-Class-Inspector
Version:        1.36
Release:        1%{?dist}
Group:          Development/Libraries
URL:            https://metacpan.org/pod/Class::Inspector
Source0:        https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/Class-Inspector-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl >= 5.42.2
Requires:       perl >= 5.42.2

%description
Class::Inspector allows to get information about a loaded class. Most or all of this information can be
   found in other ways, but they aren't always very friendly, and usually involve a relatively high level
   of Perl wizardry, or strange and unusual looking code. Class::Inspector attempts to provide an easier,
   more friendly interface to this information.

%prep
%autosetup -n Class-Inspector-%{version}
rm -rf Class-Inspector-%{version}/author.yml \
       Class-Inspector-%{version}/Changes \
       Class-Inspector-%{version}/INSTALL \
       Class-Inspector-%{version}/ \
       Class-Inspector-%{version}/Changes \
       Class-Inspector-%{version}/Changes \

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
#%{perl_vendorlib}/File/Which.pm
%{_mandir}/man3/Class::Inspector.3.gz
%{_mandir}/man3/Class::Inspector::Functions.3.gz

%changelog
* Thu Apr 30 2026 Dweep Advani <dweep.advani@broadcom.com> 1.36-1
- Introduce Class::Insector needed by File::ShareDir
