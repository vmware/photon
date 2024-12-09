# Got the intial spec from Fedora and modified it
Summary:       Internationalization library for Perl, compatible with gettext
Name:          perl-libintl
Version:       1.32
Release:       3%{?dist}
Group:         Development/Libraries
URL:           http://search.cpan.org/dist/libintl-perl/
Source0:       https://cpan.metacpan.org/authors/id/G/GU/GUIDO/libintl-perl-%{version}.tar.gz
%define sha512 libintl-perl=fca6c8863dfd36c7604bc80a401e825eb707bc75016521c09006c34c170a41b009d30ec93d7e2a7f61caa1dbdf0333511c3d515d4fdc0fea32242eca68a7e35d

Source1: license.txt
%include %{SOURCE1}
Vendor:        VMware, Inc.
Distribution:  Photon
Requires:      perl
Provides:      perl-libintl-perl = %{version}-%{release}
BuildRequires: perl

%description
The package libintl-perl is an internationalization library for Perl that
aims to be compatible with the Uniforum message translations system as
implemented for example in GNU gettext.

%prep
%autosetup -n libintl-perl-%{version}
find -type f -exec chmod -x {} \;
find lib/Locale gettext_xs \( -name '*.pm' -o -name '*.pod' \) \
    -exec sed -i -e '/^#! \/bin\/false/d' {} \;

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f \( -name .packlist -o \
                             -name '*.bs' -size 0 \) -exec rm -f {} ';'
chmod -R u+w %{buildroot}/*

%check
make %{?_smp_mflags} test

%files
%{perl_vendorlib}/Locale/
%{perl_vendorarch}/auto/Locale/
%{_mandir}/man?/*

%changelog
*   Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 1.32-3
-   Release bump for SRP compliance
*   Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 1.32-2
-   Rebuild for perl version upgrade to 5.36.0
*   Wed Aug 17 2022 Gerrit Photon <photon-checkins@vmware.com> 1.32-1
-   Automatic Version Bump
*   Thu Aug 20 2020 Gerrit Photon <photon-checkins@vmware.com> 1.31-1
-   Automatic Version Bump
*   Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.29-1
-   Update to version 1.29
*   Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> 1.26-1
-   upgrade for 2.0
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.24-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.24-1
-   Upgraded to version 1.24
*   Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.23-1
-   Initial version.
