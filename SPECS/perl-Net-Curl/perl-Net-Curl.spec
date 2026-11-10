%global build_if %{photon_subrelease} >= 91

Summary:    Perl extension interface for libcurl
Name:       perl-Net-Curl
Version:    0.58
Release:    3%{?dist}
Group:      Development/Perl
Url:        https://metacpan.org/release/Net-Curl
Vendor:     VMware, Inc.
Distribution: Photon

Source0: https://cpan.metacpan.org/modules/by-module/Net/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

# Taken from Fedora
Patch0: 0001-Fix-compatibility-crashes-and-test-failures-with-modern-libcurl.patch

BuildRequires: perl
BuildRequires: curl-devel

Requires: perl
Requires: curl-libs

Obsoletes: perl-WWW-Curl
Provides: perl-WWW-Curl

%description
Net::Curl is a Perl extension interface for libcurl.

%prep
%autosetup -p1

%build
perl Makefile.PL INSTALLDIRS=vendor
%make_build

%install
%make_install
find %{buildroot} -name 'perllocal.pod' -delete
rm -r %{buildroot}%{_mandir}

%files
%defattr(-,root,root)
%{perl_vendorarch}/Net
%{perl_vendorarch}/auto

%changelog
* Wed Nov 04 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.58-3
- extend release to 91
* Mon Aug 24 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.58-2
- Obsolete perl-WWW-curl
* Wed Jun 10 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 0.58-1
- Initial version. Needed by openssl-perl.
