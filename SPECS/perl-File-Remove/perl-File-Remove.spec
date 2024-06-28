Name:       perl-File-Remove
Version:    1.61
Release:    1%{?dist}
Summary:    Convenience module for removing files and directories
License:    GPL-1.0-or-later OR Artistic-1.0-Perl
Group:      Development/Libraries
Vendor:     VMware, Inc.
URL:        https://metacpan.org/release/File-Remove
Distribution: Photon

Source0: https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/File-Remove-%{version}.tar.gz
%define sha512 File-Remove=2ff999f7d71349b7e4a7db8728cfe2b5669c76fb27ca42fe006b0e0061bb73a29d556f3e3da88c004a4dd23bf2d9e12a1e1054b85237e8c14fb2b58c1086971f

BuildRequires:  perl
BuildRequires:  make

BuildArch:  noarch

Requires: perl

%description
%{summary}

%prep
%autosetup -p1 -n File-Remove-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install} %{?_smp_mflags}
%{_fixperms} "%{buildroot}"/*

%check
%make_build test

%files
%doc Changes README
%license LICENSE
%{perl_vendorlib}/File
%{_mandir}/man3/*

%changelog
* Sun Oct 15 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.61-1
- Initial version, needed by perl-Module-Install.
