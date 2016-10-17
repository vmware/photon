# Got the intial spec from Fedora and modified it
Summary:        YAML Ain't Markup Language (tm)
Name:           perl-YAML
Version:        1.15
Release:        3%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/YAML/
Source0:        http://search.cpan.org/CPAN/authors/id/I/IN/INGY/YAML-%{version}.tar.gz
%define sha1 YAML=c297e548f0398f2cbd93ce593be083517538f5f5
Vendor:		VMware, Inc.
Distribution:	Photon
BuildArch:      noarch
BuildRequires:	perl
Requires:	perl

# Filter private provides:
# perl(yaml_mapping) perl(yaml_scalar) perl(yaml_sequence)
%global __provides_exclude ^perl\\(yaml_

%description
The YAML.pm module implements a YAML Loader and Dumper based on the
YAML 1.0 specification. http://www.yaml.org/spec/
YAML is a generic data serialization language that is optimized for
human readability. It can be used to express the data structures of
most modern programming languages, including Perl.
For information on the YAML syntax, please refer to the YAML
specification.

%prep
%setup -q -n YAML-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name 'perllocal.pod' -delete

%check
export PERL_MM_USE_DEFAULT=1
cpan Test::YAML
make %{?_smp_mflags} test

%files
%dir %{perl_vendorlib}/YAML/
%dir %{perl_vendorlib}/YAML/Dumper/
%dir %{perl_vendorlib}/YAML/Loader/
%doc %{perl_vendorlib}/YAML.pod
%doc %{perl_vendorlib}/YAML/Any.pod
%doc %{perl_vendorlib}/YAML/Dumper.pod
%doc %{perl_vendorlib}/YAML/Dumper/Base.pod
%doc %{perl_vendorlib}/YAML/Error.pod
%doc %{perl_vendorlib}/YAML/Loader.pod
%doc %{perl_vendorlib}/YAML/Loader/Base.pod
%doc %{perl_vendorlib}/YAML/Marshall.pod
%doc %{perl_vendorlib}/YAML/Node.pod
%doc %{perl_vendorlib}/YAML/Tag.pod
%doc %{perl_vendorlib}/YAML/Types.pod
%{perl_vendorlib}/YAML.pm
%{perl_vendorlib}/YAML/Any.pm
%{perl_vendorlib}/YAML/Dumper.pm
%{perl_vendorlib}/YAML/Dumper/Base.pm
%{perl_vendorlib}/YAML/Error.pm
%{perl_vendorlib}/YAML/Loader.pm
%{perl_vendorlib}/YAML/Loader/Base.pm
%{perl_vendorlib}/YAML/Marshall.pm
%{perl_vendorlib}/YAML/Mo.pm
%{perl_vendorlib}/YAML/Node.pm
%{perl_vendorlib}/YAML/Tag.pm
%{perl_vendorlib}/YAML/Types.pm
%{_mandir}/man3/YAML.3*
%{_mandir}/man3/YAML::Any.3*
%{_mandir}/man3/YAML::Dumper.3*
%{_mandir}/man3/YAML::Dumper::Base.3*
%{_mandir}/man3/YAML::Error.3*
%{_mandir}/man3/YAML::Loader.3*
%{_mandir}/man3/YAML::Loader::Base.3*
%{_mandir}/man3/YAML::Marshall.3*
%{_mandir}/man3/YAML::Node.3*
%{_mandir}/man3/YAML::Tag.3*
%{_mandir}/man3/YAML::Types.3*

%changelog
*       Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.15-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.15-2
-	GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.15-1
-   Updated to version 1.15
*	Mon Feb 01 2016 Anish Swaminathan <anishs@vmware.com> 1.14-2
-	Fix for multithreaded perl
*	Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 1.14-1
-	Initial version.



