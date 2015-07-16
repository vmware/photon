# Got the intial spec from Fedora and modified it
Summary:        Read/Write YAML files with as little code as possible
Name:           perl-YAML-Tiny
Version:        1.66
Release:        1%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/YAML-Tiny/
Source0:        http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/YAML-Tiny-%{version}.tar.gz
%define sha1 YAML-Tiny=7fb62ca3dce1ba0310e31946d4a66ef14952e7fc
Vendor:		VMware, Inc.
Distribution:	Photon
BuildArch:      noarch
BuildRequires:  perl
Requires:	perl
%description
YAML::Tiny is a Perl class for reading and writing YAML-style files,
written with as little code as possible, reducing load time and
memory overhead.

%prep
%setup -q -n YAML-Tiny-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
make test

%files
%{perl_vendorlib}/YAML/
%{_mandir}/man3/YAML::Tiny.3*

%changelog
*	Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.66-1
-	Initial version.
