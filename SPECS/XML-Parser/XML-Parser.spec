Summary:	XML-Parser perl module
Name:		XML-Parser
Version:	2.41
Release:	3%{?dist}
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
if [ -e %{_libdir}/perl5/5.22.1/x86_64-linux-thread-multi/perllocal.pod ]; then
cat %{buildroot}/%{_libdir}/perl5/5.22.1/x86_64-linux-thread-multi/perllocal.pod >> %{_libdir}/perl5/5.22.1/x86_64-linux-thread-multi/perllocal.pod
fi
rm %{buildroot}/%{_libdir}/perl5/5.22.1/x86_64-linux-thread-multi/perllocal.pod
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
%defattr(-,root,root)
%{_libdir}/perl5/*
%{_mandir}/man3/*
%changelog
*	Mon Feb 01 2016 Anish Swaminathan <anishs@vmware.com> 2.41-3
-	Fix for multithreaded perl
*	Wed Jan 13 2016 Anish Swaminathan <anishs@vmware.com> 2.41-2
-	Fix for new perl
*	Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 2.41-1
-	Initial build. First version
