Summary:	Program to generate documenation
Name:		gtk-doc
Version:	1.33.2
Release:	2%{?dist}
License:	GPLv2+
URL:		http://www.gnu.org/software/%{name}
Source0:	http://ftp.acc.umu.se/pub/gnome/sources/gtk-doc/1.33/gtk-doc-%{version}.tar.xz
%define sha512  gtk-doc=f50f68ab6b4bc59f55e84b49c1481f05700171cbf79eca9ba8f3a142a30a4ba88fe096983ebb8d117a9ef8bcea40934674096683d956f5c54cae457d31f651ab
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:	Photon
Requires:	libxslt
Requires:	docbook-xml
Requires:	docbook-xsl
BuildRequires:	docbook-xml >= 4.5
BuildRequires:	docbook-xsl >= 1.78.1
BuildRequires:	itstool >= 2.0.2
BuildRequires:	libxslt >= 1.1.28
BuildRequires:	itstool
BuildRequires:  which
BuildRequires:	cmake
BuildRequires:	check
BuildRequires:	python3-devel
BuildRequires:	python3-libs
Requires:       python3-Pygments
Requires:	python3
Provides:	perl(gtkdoc-common.pl)
BuildArch:      noarch

%description
The GTK-Doc package contains a code documenter. This is useful for extracting
specially formatted comments from the code to create API documentation.

%prep
%autosetup -p1

%build
./autogen.sh
%configure
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} sysconfdir=%{_sysconfdir} datadir=%{_datadir} install

%check
cd tests && make check-TESTS

%files
%defattr(-,root,root)
%{_bindir}/*
/usr/share/*

%changelog
*   Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.33.2-2
-   Bump version as a part of libxslt upgrade
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.33.2-1
-   Automatic Version Bump
*   Mon Oct 5 2020 Michelle Wang <michellew@vmware.com> 1.33.0-1
-   Update to version 1.33.0
*   Wed Aug 26 2020 Keerthana K <keerthanak@vmware.com> 1.32-1
-   Update to version 1.32.
*   Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com>  1.29-1
-   Upgrade to 1.29
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.25-2
-   Fix arch
*   Fri Mar 24 2017 Dheeraj Shetty <dheerajs@vmware.com>  1.25-1
-   Upgrade to 1.25
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.24-3
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.24-1
-   Upgrade to 1.24
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.21.1-2
-   Updated group.
*   Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 1.21-1
-   Initial build. First version
