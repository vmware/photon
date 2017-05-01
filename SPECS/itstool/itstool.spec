Summary:	Itstool-2.0.2
Name:		itstool
Version:	2.0.2
Release:	4%{?dist}
License:	GPLv3+
URL:		http://itstool.org
Source0:	http://files.itstool.org/itstool/%{name}-%{version}.tar.bz2
%define sha1 itstool=5084a2cecca8d70d184f22d2aecf5e2cb715917f
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	docbook-xml >= 4.5
BuildRequires:	python2 >= 2.7.8
BuildRequires:	python2-libs >= 2.7.8
Requires:	python2
Requires:	libxml2-python
%description
Itstool extracts messages from XML files and outputs PO template files, then merges 
translations from MO files to create translated XML files. It determines what 
to translate and how to chunk it into messages using the W3C Internationalization Tag Set (ITS).
%prep
%setup -q
%build
./configure --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
%defattr(-,root,root)
%{_bindir}/*
/usr/share/%{name}/*
%{_mandir}/man1/*
%changelog
*	Mon May 1 2017 Divya Thaluru <dthaluru@vmware.com> 2.0.2-4
-	Added runtime dependencies for itstool
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.2-3
-	GA - Bump release of all rpms
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.0.2-2
-   Updated group.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.0.2-1
-	Initial build. First version
