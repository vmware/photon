Summary:	Itstool-2.0.2
Name:		itstool
Version:	2.0.2
Release:	2%{?dist}
License:	GPLv3+
URL:		http://itstool.org
Source0:	http://files.itstool.org/itstool/%{name}-%{version}.tar.bz2
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	docbook-xml >= 4.5
BuildRequires:	python2 >= 2.7.8
BuildRequires:	python2-libs >= 2.7.8
Requires:	python2
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
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.0.2-2
-   Updated group.
*	Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.0.2-1
-	Initial build. First version
