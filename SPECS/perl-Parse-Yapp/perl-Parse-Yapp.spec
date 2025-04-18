Summary:        Perl extension for generating and using LALR parsers
Name:           perl-Parse-Yapp
Version:        1.21
Release:        4%{?dist}
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Parse-Yapp
Group:          Development/Libraries/Perl
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://www.cpan.org/authors/id/W/WB/WBRASWELL/Parse-Yapp-%{version}.tar.gz
%define sha512 Parse-Yapp=dbf6182d4813ff7e355ea1713c748bfdf8290040a93f123acec645c7a1733fe457ab6e0ab51c4ec83cf82bc43d7fb35cbf89875df7b5c2ffc9635e85458cfeee

BuildArch:      noarch

BuildRequires:  coreutils >= 9.1-7
BuildRequires:  make
BuildRequires:  perl

Requires:       perl

%description
Parse::Yapp (Yet Another Perl Parser compiler) is a collection of modules that
let you generate and use yacc like thread safe (reentrant) parsers with perl
object oriented interface.  The script yapp is a front-end to the Parse::Yapp
module and let you easily create a Perl OO parser from an input grammar file.

%prep
%autosetup -p1 -n Parse-Yapp-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
%make_build

%install
make pure_install DESTDIR=%{buildroot} %{?_smp_mflags}
chmod -R u+w %{buildroot}/*

%if 0%{?with_check}
%check
make test %{?_smp_mflags}
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/yapp
%{perl_vendorlib}/Parse/
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*

%changelog
* Wed Oct 16 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.21-4
- Require coreutils only
* Sun Feb 12 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.21-3
- Fix build requires
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 1.21-2
- Perl versioin upgrade to 5.36.0
* Fri Mar 13 2020 Shreyas B. <shreyasb@vmware.com> 1.21-1
- Initial version.
