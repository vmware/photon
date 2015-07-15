Summary:	XML-Parser perl module
Name:		XML-Parser
Version:	2.41
Release:	1%{?dist}
License:	GPL+
URL:		http://search.cpan.org/~toddr/%{name}-%{version}/
Source0:		http://search.cpan.org/CPAN/authors/id/T/TO/TODDR/%{name}-%{version}.tar.gz
%define sha1 XML-Parser=68c7ee61b413c2e8255699b1987fca598e0a39d8
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	expat
Requires:	expat
%description
The XML::Parser module is a Perl extension interface to James Clark's XML parser, expat
%prep
%setup -q
%build
perl Makefile.PL --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
if [ -e %{_libdir}/perl5/5.18.2/x86_64-linux/perllocal.pod ]; then
cat %{buildroot}/%{_libdir}/perl5/5.18.2/x86_64-linux/perllocal.pod >> %{_libdir}/perl5/5.18.2/x86_64-linux/perllocal.pod
fi
rm %{buildroot}/%{_libdir}/perl5/5.18.2/x86_64-linux/perllocal.pod
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
%defattr(-,root,root)
%{_libdir}/perl5/*
%{_mandir}/man3/*
%changelog
*	Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 2.41-1
-	Initial build. First version
