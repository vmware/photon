Summary:        SSL sockets with IO::Socket interface
Name:           perl-IO-Socket-SSL
Version:        2.068
Release:        2%{?dist}
License:        Perl Artistic License 2.0
Group:          Development/Libraries
URL:            http://search.cpan.org/~sullr/IO-Socket-SSL-2.024/lib/IO/Socket/SSL.pod
Vendor:         VMware, Inc.
Distribution:   Photon

Source:         https://cpan.metacpan.org/authors/id/S/SU/SULLR/IO-Socket-SSL-%{version}.tar.gz
%define sha1 IO-Socket-SSL=9d7583f5fb80085795ae55471adbc1840ca749fa

BuildArch:      noarch

Requires:       perl
Requires:       perl-Net-SSLeay

BuildRequires:  perl
BuildRequires:  perl-Net-SSLeay

%description
IO::Socket::SSL makes using SSL/TLS much easier by wrapping the necessary functionality into the familiar IO::Socket interface and providing secure defaults whenever possible. This way, existing applications can be made SSL-aware without much effort, at least if you do blocking I/O and don't use select or poll.

%prep
%autosetup -p1 -n IO-Socket-SSL-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot} %{?_smp_mflags}
find %{buildroot} -type f \( -name .packlist -o \
            -name '*.bs' -size 0 \) -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%check
%if 0%{?with_check:1}
make test %{?_smp_mflags}
%endif

%files
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
* Fri Jan 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.068-2
- Bump version as a part of perl-Net-SSLeay version upgrade
* Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 2.068-1
- Automatic Version Bump
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 2.060-1
- Update to version 2.060
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.047-2
- Ensure non empty debuginfo
* Mon Apr 3 2017 Robert Qi <qij@vmware.com> 2.047-1
- Update to 2.047
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.024-2
- GA - Bump release of all rpms
* Mon Mar 28 2016 Mahmoud Bassiouny <mbassiounu@vmware.com> 2.024-1
- Initial version.
