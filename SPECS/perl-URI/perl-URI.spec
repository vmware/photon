%global build_if %{photon_subrelease} >= 91

Summary:        A Perl module implementing URI parsing and manipulation
Name:           perl-URI
Version:        5.34
Release:        1%{?dist}
Group:          Development/Libraries
URL:            https://metacpan.org/release/URI
Source0:        https://cpan.metacpan.org/modules/by-module/URI/URI-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  perl >= 5.42.2
BuildRequires:  make

Requires:       perl >= 5.42.2

%description
This module implements the URI class. Objects of this class represent
"Uniform Resource Identifier references" as specified in RFC 2396
(andupdated by RFC 2732).

%global debug_package %{nil}

%prep
%autosetup -n URI-%{version}
%if 0%{?with_check} == 0
  for f in t xt; do
    sed -i -E "/^$f\\/.*$/d" MANIFEST
    rm -rf "$f"
  done
%endif

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=true NO_PERLLOCAL=true
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%files
%license LICENSE
%doc Changes CONTRIBUTING.md README uri-test
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Thu Apr 09 2026 Dweep Advani <dweep.advani@broadcom.com> 5.34-1
- Upgrade to 5.34
* Wed Jun 11 2025 Dweep Advani <dweep.advani@broadcom.com> 5.32-1
- Upgrade to 5.32
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 5.17-2
- Release bump for SRP compliance
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 5.17-1
- Version upgrade to 5.17
* Fri Apr 30 2021 Susant Sahani <ssahani@vmware.com> 5.09-1
- Initial version.
