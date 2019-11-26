Summary:	Intltool
Name:		intltool
Version:	0.51.0
Release:	4%{?dist}
License:	GPLv2+
URL:		https://freedesktop.org/wiki/Software/intltool/
Source0:	https://launchpad.net/intltool/+download/%{name}-%{version}.tar.gz
%define sha1 intltool=a0c3bcb99d1bcfc5db70f8d848232a47c47da090
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
Requires: 	XML-Parser
BuildRequires:	XML-Parser
BuildArch:      noarch

%description
The Intltool is an internationalization tool used for extracting translatable strings from source files.
%prep
%setup -q
%build
%configure
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -v -Dm644 doc/I18N-HOWTO %{buildroot}/%{_docdir}/%{name}-%{version}/I18N-HOWTO

%check
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}/I18N-HOWTO
%{_bindir}/*
%{_datadir}/aclocal/intltool.m4
%{_datadir}/intltool/*
%{_mandir}/man8/*
%changelog
*   Thu Nov 15 2018 Alexey Makhalov <amakhalov@vmware.com> 0.51.0-4
-   Cross compilation support
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.51.0-3
-   Fix arch
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.51.0-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  0.51.0-1
-   Upgrade to 0.51.0
*   Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 0.50.2-1
-   Initial version
