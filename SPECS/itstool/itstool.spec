Summary:        Itstool-2.0.6
Name:           itstool
Version:        2.0.6
Release:        3%{?dist}
License:        GPLv3+
URL:            http://itstool.org
Source0:        http://files.itstool.org/itstool/%{name}-%{version}.tar.bz2
%define sha1 itstool=9a7a3cd6e33763f6f369a907e79da98cc47b86e7
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  docbook-xml >= 4.5
BuildRequires:  libxml2
BuildRequires:  python3-libxml2
BuildRequires:  python3
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libxml2
BuildArch:      noarch

%description
Itstool extracts messages from XML files and outputs PO template files, then merges
translations from MO files to create translated XML files. It determines what
to translate and how to chunk it into messages using the W3C Internationalization Tag Set (ITS).
%prep
%autosetup -p1

%build
export PYTHON=/usr/bin/python3
%configure
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
/usr/share/%{name}/*
%{_mandir}/man1/*

%changelog
*   Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 2.0.6-3
-   Release bump up to use libxml2 2.9.12-1.
*   Mon Jul 20 2020 Tapas Kundu <tkundu@vmware.com> 2.0.6-2
-   Build with python3
-   Mass removal python2
*   Tue Jul 07 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.6-1
-   Automatic Version Bump
*   Mon May 1 2017 Divya Thaluru <dthaluru@vmware.com> 2.0.2-5
-   Added runtime dependencies for itstool
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.2-4
-   Fix arch
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.2-3
-   GA - Bump release of all rpms
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.0.2-2
-   Updated group.
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.0.2-1
-   Initial build. First version
