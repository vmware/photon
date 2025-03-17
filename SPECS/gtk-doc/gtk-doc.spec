Summary:    Program to generate documenation
Name:       gtk-doc
Version:    1.33.2
Release:    5%{?dist}
URL:        http://www.gnu.org/software/%{name}
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://ftp.acc.umu.se/pub/gnome/sources/gtk-doc/1.33/gtk-doc-%{version}.tar.xz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:  docbook-xml >= 4.5
BuildRequires:  docbook-xsl >= 1.78.1
BuildRequires:  itstool >= 2.0.2
BuildRequires:  libxslt-devel >= 1.1.28
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

BuildArch:      noarch

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
%make_install %{?_smp_mflags}

%check
cd tests && make check-TESTS %{?_smp_mflags}

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1.33.2-5
- Release bump for SRP compliance
* Tue Nov 05 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.33.2-4
- Release bump for SRP compliance
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.33.2-3
- Bump version as a part of libxslt upgrade
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.33.2-2
- Bump version as a part of libxslt upgrade
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.33.2-1
- Automatic Version Bump
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
