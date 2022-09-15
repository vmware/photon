Summary:    Program to generate documenation
Name:       gtk-doc
Version:    1.33.0
Release:    1%{?dist}
License:    GPLv2+
URL:        http://www.gnu.org/software/%{name}
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://ftp.acc.umu.se/pub/gnome/sources/gtk-doc/1.33/gtk-doc-%{version}.tar.xz
%define sha512 %{name}=734440b61edc4101fbb34397036ddafa4003aa31f0a2258e0a855a563460d8e626588cb513b1a7850f6f843bbeb0a626ed33266a4dead5c10a4930fe688cfec9

BuildRequires:  docbook-xml >= 4.5
BuildRequires:  docbook-xsl >= 1.78.1
BuildRequires:  itstool >= 2.0.2
BuildRequires:  libxslt >= 1.1.28
BuildRequires:  itstool
BuildRequires:  which
BuildRequires:  cmake
BuildRequires:  check-devel
BuildRequires:  python3-devel

Requires:   libxslt
Requires:   docbook-xml
Requires:   docbook-xsl
Requires:   python3-Pygments
Requires:   python3
Provides:   perl(gtkdoc-common.pl)

BuildArch:  noarch

%description
The GTK-Doc package contains a code documenter. This is useful for extracting
specially formatted comments from the code to create API documentation.

%prep
%autosetup -p1

%build
sh ./autogen.sh
%configure
%make_build

%install
%make_install %{?_smp_mflags} DESTDIR=%{buildroot} sysconfdir=%{_sysconfdir} datadir=%{_datadir}

%check
cd tests && make check-TESTS %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*

%changelog
* Mon Oct 5 2020 Michelle Wang <michellew@vmware.com> 1.33.0-1
- Update to version 1.33.0
* Wed Aug 26 2020 Keerthana K <keerthanak@vmware.com> 1.32-1
- Update to version 1.32.
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com>  1.29-1
- Upgrade to 1.29
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.25-2
- Fix arch
* Fri Mar 24 2017 Dheeraj Shetty <dheerajs@vmware.com>  1.25-1
- Upgrade to 1.25
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.24-3
- GA - Bump release of all rpms
* Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.24-1
- Upgrade to 1.24
* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.21.1-2
- Updated group.
* Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 1.21-1
- Initial build. First version
