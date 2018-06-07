# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

Summary:        Cross-platform path specification manipulation for Perl
Name:           perl-Path-Class
Version:        0.37
Release:        2%{?dist}
URL:            http://search.cpan.org/~kwilliams/Path-Class-0.37/
License:        The Perl 5 License (Artistic 1 & GPL 1)
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source:         http://search.cpan.org/CPAN/authors/id/K/KW/KWILLIAMS/Path-Class-%{version}.tar.gz
%define sha1    Path-Class=448cc1089add95d6a616a8e22adbde83dcb8f562

BuildArch:      x86_64
Requires:       perl
BuildRequires:  perl

%description
Path::Class is a module for manipulation of file and directory specifications (strings describing their locations, like '/home/ken/foo.txt' or 'C:\Windows\Foo.txt') in a cross-platform manner. It supports pretty much every platform Perl runs on, including Unix, Windows, Mac, VMS, Epoc, Cygwin, OS/2, and NetWare.

The well-known module File::Spec also provides this service, but it's sort of awkward to use well, so people sometimes avoid it, or use it in a way that won't actually work properly on platforms significantly different than the ones they've tested their code on.

%prep
%setup -q -n Path-Class-%{version}

%build
env PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
make test

%files
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
*   Wed Jun 06 2018 Xiaolin Li <xiaolinl@vmware.com> 0.37-2
-   Bump release after upgraded perl to 5.24.1
*   Wed Apr 19 2017 Xiaolin Li <xiaolinl@vmware.com> 0.37-1
-   Initial version.
