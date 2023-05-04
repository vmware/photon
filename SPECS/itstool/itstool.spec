Summary:        Itstool-2.0.6
Name:           itstool
Version:        2.0.6
Release:        4%{?dist}
License:        GPLv3+
URL:            http://itstool.org
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://files.itstool.org/itstool/%{name}-%{version}.tar.bz2
%define sha512 %{name}=51058bdcb208f6fb84810f71f9bf67e42b00bf157a9756be45f060849c0aff36f695f4403404193720d4446818fa77de61fa94eed9e8789d26c07a2926072eb7

BuildRequires:  docbook-xml >= 4.5
BuildRequires:  libxml2-devel
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
%make_build

%install
%make_install %{?_smp_mflags}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/%{name}/*
%{_mandir}/man1/*

%changelog
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.6-4
- Bump up to compile with python 3.10
* Thu Nov 18 2021 Nitesh Kumar <kunitesh@vmware.com> 2.0.6-3
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
