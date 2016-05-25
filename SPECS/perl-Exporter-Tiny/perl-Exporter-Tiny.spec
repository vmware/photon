# Got the intial spec from Fedora and modified it
Summary:	An exporter with the features of Sub::Exporter but only core dependencies
Name:		perl-Exporter-Tiny
Version:	0.042
Release:	2%{?dist}
License:	(GPL+ or Artistic) and Public Domain and (GPL+ or Artistic or CC-BY-SA)
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Exporter-Tiny/
Source0:	http://search.cpan.org/CPAN/authors/id/T/TO/TOBYINK/Exporter-Tiny-%{version}.tar.gz
%define sha1 Exporter-Tiny=3a3ac1affabcfce1d1bf8cffee2e7a8c78780e54
Vendor:		VMware, Inc.
Distribution:	Photon
BuildArch:	noarch
BuildRequires:	perl
Requires:	perl

%description
Exporter::Tiny supports many of Sub::Exporter's external-facing features
including renaming imported functions with the -as, -prefix and -suffix
options; explicit destinations with the into option; and alternative
installers with the installer option. But it's written in only about 40%%
as many lines of code and with zero non-core dependencies.

Its internal-facing interface is closer to Exporter.pm, with configuration
done through the @EXPORT, @EXPORT_OK and %%EXPORT_TAGS package variables.

Exporter::Tiny performs most of its internal duties (including resolution of
tag names to sub names, resolution of sub names to coderefs, and installation
of coderefs into the target package) as method calls, which means they can be
overridden to provide interesting behavior.

%prep
%setup -q -n Exporter-Tiny-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
make test

%clean
rm -rf %{buildroot}

%files
%{perl_vendorlib}/Exporter/
%{_mandir}/man3/Exporter::Tiny.3*
%{_mandir}/man3/Exporter::Shiny.3*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.042-2
-	GA - Bump release of all rpms
*	Fri Apr 3 2015 Divya Thaluru <dthaluru@vmware.com> 0.042-1
-	Initial version.
