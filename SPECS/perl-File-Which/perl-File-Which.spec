Summary:        File-Which
Name:           perl-File-Which
Version:        1.23
Release:        1%{?dist}
License:        The Perl 5 License (Artistic 1 & GPL 1)
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/File-Which/
Source0:        https://cpan.metacpan.org/authors/id/P/PL/PLICEASE/File-Which-%{version}.tar.gz
%define sha1 File-Which=3a1b54e0a4e470e62958749cffcf87bad027bfb4
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl
Requires:       perl

%description
File::Which finds the full or relative paths to executable programs on
    the system. This is normally the function of which utility. which is
    typically implemented as either a program or a built in shell command.
    On some platforms, such as Microsoft Windows it is not provided as part
    of the core operating system. This module provides a consistent API to
    this functionality regardless of the underlying platform.

    The focus of this module is correctness and portability. As a
    consequence platforms where the current directory is implicitly part of
    the search path such as Microsoft Windows will find executables in the
    current directory, whereas on platforms such as UNIX where this is not
    the case executables in the current directory will only be found if the
    current directory is explicitly added to the path.

    If you need a portable which on the command line in an environment that
    does not provide it, install App::pwhich which provides a command line
    interface to this API.
%prep
%setup -q -n File-Which-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
make test

%files
%{perl_vendorlib}/*
%{perl_vendorlib}/File/Which.pm
%{_mandir}/man3/File::Which.3.gz


%changelog
*   Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 1.23-1
-   Automatic Version Bump
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.22-1
-   Update to version 1.22
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.21-2
-   GA - Bump release of all rpms
*   Thu Mar 3 2016 Xiaolin Li <xiaolinl@vmware.com> 1.21-1
-   Initial version.
