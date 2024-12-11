Summary:        Itstool-2.0.6
Name:           itstool
Version:        2.0.7
Release:        5%{?dist}
URL:            http://itstool.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://files.itstool.org/itstool/%{name}-%{version}.tar.bz2
%define sha512  itstool=710c188e518a7eccbf9d31df59692fd6acc79430589a93ef4333f33f74440c311c340614ca74cc43191830567a98024d0981325ccd83a8fd9b75410d9dd91992

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  docbook-xml >= 4.5
BuildRequires:  libxml2
BuildRequires:  python3-libxml2
BuildRequires:  python3-devel

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
export PYTHON=%{python3}

%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/%{name}/*
%{_mandir}/man1/*

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 2.0.7-5
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.7-4
- Release bump for SRP compliance
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.0.7-3
- Bump version as a part of libxml2 upgrade
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.7-2
- Update release to compile with python 3.11
* Sun May 29 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.7-1
- Automatic Version Bump
* Wed Nov 17 2021 Nitesh Kumar <kunitesh@vmware.com> 2.0.6-3
- Release bump up to use libxml2 2.9.12-1.
* Mon Jul 20 2020 Tapas Kundu <tkundu@vmware.com> 2.0.6-2
- Build with python3
- Mass removal python2
* Tue Jul 07 2020 Gerrit Photon <photon-checkins@vmware.com> 2.0.6-1
- Automatic Version Bump
* Mon May 1 2017 Divya Thaluru <dthaluru@vmware.com> 2.0.2-5
- Added runtime dependencies for itstool
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.2-4
- Fix arch
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.0.2-3
- GA - Bump release of all rpms
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.0.2-2
- Updated group.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.0.2-1
- Initial build. First version
