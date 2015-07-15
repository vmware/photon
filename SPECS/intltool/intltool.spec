Summary:	Intltool-0.50.2 
Name:		intltool
Version:	0.50.2
Release:	1%{?dist}
License:	GPLv2+
URL:		http://freedesktop.org/wiki/Software/%{name}l/
Source0:	http://launchpad.net/intltool/trunk/0.50.2/+download/%{name}-%{version}.tar.gz
%define sha1 intltool=7fddbd8e1bf94adbf1bc947cbf3b8ddc2453f8ad
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
Requires: 	XML-Parser
BuildRequires:	XML-Parser
%description
The Intltool is an internationalization tool used for extracting translatable strings from source files.
%prep
%setup -q
%build
./configure --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -v -Dm644 doc/I18N-HOWTO %{buildroot}/%{_docdir}/%{name}-%{version}/I18N-HOWTO
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
%defattr(-,root,root)
%{_docdir}/%{name}-%{version}/I18N-HOWTO
%{_bindir}/*
%{_datadir}/aclocal/intltool.m4
%{_datadir}/intltool/*
%{_mandir}/man8/*
%changelog
*	Thu Oct 23 2014 Divya Thaluru <dthaluru@vmware.com> 0.50.2-1
-	Initial version
