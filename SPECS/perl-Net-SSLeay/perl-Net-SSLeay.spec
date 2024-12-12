Summary:        Perl extension for using OpenSSL
Name:           perl-Net-SSLeay
Version:        1.92
Release:        2%{?dist}
Group:          Development/Libraries
URL:            https://metacpan.org/pod/Net::SSLeay
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://cpan.metacpan.org/authors/id/C/CH/CHRISN/Net-SSLeay-%{version}.tar.gz
%define sha512  Net-SSLeay=e9d9161ebeb7be90f4c7a0ea98f1034892ce6d33aa72872683177b19daa1f4c5819f85ea9a052a076ec8d7c21705f6c344aef64680bc881bf3218d38e8b7b173

Source1: license.txt
%include %{SOURCE1}

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
%make_build

%install
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -delete
find %{buildroot} -type f -name '*.bs' -empty -delete

%if 0%{?with_check}
%check
# Install required modules for test - Test::Pod, Test::Exception, Test::Warn and Test::NoWarnings
export PERL_MM_USE_DEFAULT=1
echo "yes" | cpan -a
cpan -i Test::Pod Test::Exception Test::Warn Test::NoWarnings
make test %{?_smp_mflags}
%endif

%files
%defattr(-,root,root)
%{perl_vendorlib}/*
%{_mandir}/man?/*

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.92-2
- Release bump for SRP compliance
* Thu Dec 08 2022 Gerrit Photon <photon-checkins@vmware.com> 1.92-1
- Automatic Version Bump
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
