# Got the intial spec from Fedora and modified it
Summary:        Easy-to-use OO interface to DBI
Name:           perl-DBIx-Simple
Version:        1.37
Release:        3%{?dist}
License:        Public Domain
Group:          Development/Libraries

Source0:        https://cpan.metacpan.org/authors/id/J/JU/JUERD/DBIx-Simple-%{version}.tar.gz
%define sha1 DBIx-Simple=7ca4c4ed5c1b6a8f32734e7d5692750b4e01aa17

URL:            http://search.cpan.org/dist/DBIx-Simple/
Vendor:         VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

BuildRequires:  perl-DBI
BuildRequires:  perl

Requires:       perl
Requires:       perl-Object-Accessor
Requires:       perl-DBI

%description
DBIx::Simple provides a simplified interface to DBI, Perl's powerful
database module.

%prep
%autosetup -p1 -n DBIx-Simple-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot} %{?_smp_mflags}
%{_fixperms} %{buildroot}/*

%check
make test %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Apr 14 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.37-3
- Fixed build issues after upgrading rpm version
* Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 1.37-2
- Rebuilding for perl 5.30.1
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.37-1
- Update to version 1.37
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.35-2
- GA - Bump release of all rpms
* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.35-1
- Initial version.
