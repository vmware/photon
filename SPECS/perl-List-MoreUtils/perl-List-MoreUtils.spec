# Got the intial spec from Fedora and modified it
Summary:       Provide the stuff missing in List::Util
Name:          perl-List-MoreUtils
Version:       0.430
Release:       2%{?dist}
Group:         Development/Libraries
URL:           http://search.cpan.org/dist/List-MoreUtils/
Source0:       https://cpan.metacpan.org/authors/id/R/RE/REHSACK/List-MoreUtils-%{version}.tar.gz
%define sha512 List-MoreUtils=bc9ff033c12251a6f0899a96da0ec8fc314ddb8d6cdf18c37fe1fdcfc38a4c95ed6f8e006bb124e77d07241ae6754f429bc2041f7772b4acfce9378a21283469

Source1: license.txt
%include %{SOURCE1}
Vendor:        VMware, Inc.
Distribution:  Photon
BuildArch:     noarch
BuildRequires: perl
Requires:      perl
BuildRequires: perl-Exporter-Tiny
Requires:      perl-Exporter-Tiny

%description
List::MoreUtils provides some trivial but commonly needed functionality
on lists that is not going to go into List::Util.

%prep
%autosetup -n List-MoreUtils-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PERLLOCAL=1 NO_PACKLIST=1
make %{?_smp_mflags}

%install
make  %{?_smp_mflags} install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete
%{_fixperms} -c %{buildroot}

%check
# Install required module List::MoreUtils::XS for maketest
export PERL_MM_USE_DEFAULT=1
echo "yes" | cpan -a
cpan -i List::MoreUtils::XS
make  %{?_smp_mflags} test

%files
%{perl_vendorlib}/List/
%{_mandir}/man3/List::MoreUtils.3*
%{_mandir}/man3/List::MoreUtils::PP.3*
%{_mandir}/man3/List::MoreUtils::Contributing.3.gz

%changelog
* Thu Dec 12 2024 Dweep Advani <dweep.advani@broadcom.com> 0.430-2
- Release bump for SRP compliance
* Thu Dec 08 2022 Gerrit Photon <photon-checkins@vmware.com> 0.430-1
- Automatic Version Bump
* Mon Aug 31 2020 Dweep Advani <dadvani@vmware.com> 0.428-3
- Rebuild for perl 5.30.1
* Mon Dec 03 2018 Dweep Advani <dadvani@vmware.com> 0.428-2
- Fix makecheck tests
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 0.428-1
- Update to version 0.428
* Wed Apr 05 2017 Robert Qi <qij@vmware.com> 0.418-1
- Update version to 0.418
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.413-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 0.413-1
- Updated to version 0.413
* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 0.410-1
- Initial version.
