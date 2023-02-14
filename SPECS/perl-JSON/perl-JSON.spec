Summary:        Perl wrapper for JSON. Provides JSON.pm
Name:           perl-JSON
Version:        4.10
Release:        1%{?dist}
License:        Perl 5 License (Artistic 1 & GPL 1)
Group:          Development/Libraries
URL:            https://metacpan.org/pod/JSON
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch

Source:         https://cpan.metacpan.org/authors/id/I/IS/ISHIGAKI/JSON-%{version}.tar.gz
%define sha512 JSON-%{version}=2aa0c40fbff23d3df84cfa729d00a32a69e06ea83d082b25b7223f90cb157fa3c2e72342fadcd2ebe09b5848a0e3a7d2caec6d1753e95952a56e3e9367f343e3

Requires:       perl >= 5.28.0
BuildRequires:  perl >= 5.28.0

# otherwise tdnf fails to install
Provides:  perl(JSON::backportPP::Boolean)

%description
This module is a thin wrapper for JSON::XS-compatible modules with a few additional features. All the backend modules convert a Perl data structure to a JSON text and vice versa. This module uses JSON::XS by default, and when JSON::XS is not available, falls back on JSON::PP, which is in the Perl core since 5.14. If JSON::PP is not available either, this module then falls back on JSON::backportPP (which is actually JSON::PP in a different .pm file) bundled in the same distribution as this module. You can also explicitly specify to use Cpanel::JSON::XS, a fork of JSON::XS by Reini Urban.

All these backend modules have slight incompatibilities between them, including extra features that other modules don't support, but as long as you use only common features (most important ones are described below), migration from backend to backend should be reasonably easy. For details, see each backend module you use.

%prep
%autosetup -n JSON-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
%make_build

%install
make pure_install %{?_smp_mflags} DESTDIR=%{buildroot}

%check
export PERL_MM_USE_DEFAULT=1
cpan Test::Fatal  Test::Requires Test::Warnings Test::Without::Module
make test %{?_smp_mflags}

%files
%{perl_vendorlib}/*
%exclude %{_mandir}/man?/*

%changelog
*   Tue Feb 14 2023 Brennan Lamoreaux <blamoreaux@vmware.com> 4.10-1
-   Initial addition
