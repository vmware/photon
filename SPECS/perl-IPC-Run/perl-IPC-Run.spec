Summary:        system() and background procs w/ piping, redirs, ptys (Unix, Win32)
Name:           perl-IPC-Run
Version:        20200505.0
Release:        1%{?dist}
URL:            https://metacpan.org/pod/IPC::Run
License:        The Perl 5 License (Artistic 1 & GPL 1)
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon
Source:         https://cpan.metacpan.org/authors/id/T/TO/TODDR/IPC-Run-%{version}.tar.gz
%define sha1    IPC-Run=297d6410a91f6dc466543476bea743a9b21df2e9

BuildArch:      noarch
Requires:       perl
BuildRequires:  perl

%description
IPC::Run allows you to run and interact with child processes using files,
pipes, and pseudo-ttys. Both system()-style and scripted usages are
supported and may be mixed. Likewise, functional and OO API styles are
both supported and may be mixed.

%prep
%setup -q -n IPC-Run-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete
# Remove anything related to Win32.  Note that there are required for the
# tests.
find %{buildroot} -name '*Win32*' -delete

%check
make test

%files
%{perl_vendorlib}/IPC/Run.pm
%{perl_vendorlib}/IPC/Run/Debug.pm
%{perl_vendorlib}/IPC/Run/IO.pm
%{perl_vendorlib}/IPC/Run/Timer.pm
%{_mandir}/man3/IPC::Run.3.gz
%{_mandir}/man3/IPC::Run::Debug.3.gz
%{_mandir}/man3/IPC::Run::IO.3.gz
%{_mandir}/man3/IPC::Run::Timer.3.gz

%changelog
*   Thu Feb 25 2021 Michael Paquier <mpaquier@vmware.com> 20200505.0-1
-   Initial version
