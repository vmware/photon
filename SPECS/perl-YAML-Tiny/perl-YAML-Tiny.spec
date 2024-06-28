# Got the intial spec from Fedora and modified it
Summary:        Read/Write YAML files with as little code as possible
Name:           perl-YAML-Tiny
Version:        1.73
Release:        3%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/YAML-Tiny/
Source0:        https://cpan.metacpan.org/authors/id/E/ET/ETHER/YAML-Tiny-%{version}.tar.gz
%define sha512  YAML-Tiny=5999e220025aa8076e5e0e9e73e80c2da21660e77f6744d73e8e29962221d02d33a36e9829c44abf7d4f45abae069d8e121c8019bd1600b7e64db5e54efd9987
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
BuildRequires:  perl
Requires:       perl
%description
YAML::Tiny is a Perl class for reading and writing YAML-style files,
written with as little code as possible, reducing load time and
memory overhead.

%prep
%autosetup -n YAML-Tiny-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make %{?_smp_mflags} pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make %{?_smp_mflags} test

%files
%{perl_vendorlib}/YAML/
%{_mandir}/man3/YAML::Tiny.3*

%changelog
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 1.73-3
- Perl version upgrade to 5.36.0
* Thu Aug 20 2020 Dweep Advani <dadvani@vmware.com> 1.73-2
- Rebuilding for perl 5.30.1
* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> 1.73-1
- Update to version 1.73
* Wed Apr 05 2017 Robert Qi <qij@vmware.com> 1.70-1
- Update version to 1.70
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.69-2
- GA - Bump release of all rpms
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.69-1
- Upgraded to version 1.69
* Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.66-1
- Initial version.
