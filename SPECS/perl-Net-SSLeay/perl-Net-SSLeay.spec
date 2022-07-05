Summary:        Perl extension for using OpenSSL
Name:           perl-Net-SSLeay
Version:        1.90
Release:        1%{?dist}
License:        Perl Artistic License 2.0
Group:          Development/Libraries
URL:            https://metacpan.org/pod/Net::SSLeay
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:         https://cpan.metacpan.org/authors/id/C/CH/CHRISN/Net-SSLeay-%{version}.tar.gz
%define sha1 Net-SSLeay=675c9df74163d48477ecf06601a589f3c3b096dd

Requires:       perl
Requires:       openssl

BuildRequires:  perl
BuildRequires:  openssl-devel

%description
Net::SSLeay module contains perl bindings to openssl (http://www.openssl.org) library.

Net::SSLeay module basically comprise of:
* High level functions for accessing web servers (by using HTTP/HTTPS)
* Low level API (mostly mapped 1:1 to openssl's C functions)
* Convenience functions (related to low level API but with more perl friendly interface)
* There is also a related module called Net::SSLeay::Handle included in this distribution that you might want to use instead. It has its own pod documentation.

%prep
%autosetup -p1 -n Net-SSLeay-%{version}

%build
env PERL_MM_USE_DEFAULT=1 perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot} %{?_smp_mflags}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete

%check
%if 0%{?with_check:1}
# Install required modules for test - Test::Pod, Test::Exception, Test::Warn and Test::NoWarnings
export PERL_MM_USE_DEFAULT=1
echo "yes" | cpan -a
cpan -i Test::Pod Test::Exception Test::Warn Test::NoWarnings
make test %{?_smp_mflags}
%endif

%files
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
* Fri Jan 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.90-1
- Upgrade to v1.90 & remove fips related instructions from spec
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.88-3
- Bump up release for openssl
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.88-2
- openssl 1.1.1
* Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 1.88-1
- Automatic Version Bump
* Mon Dec 03 2018 Dweep Advani <dadvani@vmware.com> 1.85-3
- Fixing makecheck tests
* Wed Oct 17 2018 Alexey Makhalov <amakhalov@vmware.com> 1.85-2
- Move fips logic to spec file
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.85-1
- Update to version 1.85
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.81-2
- Remove BuildArch
* Wed Apr 05 2017 Robert Qi <qij@vmware.com> 1.81-1
- Update version to 1.81
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.72-2
- GA - Bump release of all rpms
* Mon Mar 28 2016 Mahmoud Bassiouny <mbassiounu@vmware.com> 1.72-1
- Initial version.
