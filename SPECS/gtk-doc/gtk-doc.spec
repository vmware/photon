Summary:	Program to generate documenation
Name:		gtk-doc
Version:	1.29
Release:	4%{?dist}
License:	GPLv2+
URL:		http://www.gnu.org/software/%{name}
Source0:	http://ftp.gnome.org/pub/gnome/sources/gtk-doc/1.25/%{name}-%{version}.tar.xz
%define sha512  gtk-doc=97e17be2563c2c12a04394633feaf6591918968a794c38e945a65be9c2de2bed5ce586592a7fe396a1874b8e43e63d6380c6d1a3193ccb7f9bb3d3a331526421
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  docbook-xml >= 4.5
BuildRequires:  docbook-xsl >= 1.78.1
BuildRequires:  itstool >= 2.0.2
BuildRequires:  libxslt >= 1.1.28
BuildRequires:  itstool
BuildRequires:  cmake
BuildRequires:  check
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-libxml2
Requires:       python3
Requires:       libxslt
Requires:       docbook-xml
Requires:       docbook-xsl
Provides:       perl(gtkdoc-common.pl)
BuildArch:      noarch

%description
The GTK-Doc package contains a code documenter. This is useful for extracting
specially formatted comments from the code to create API documentation.
%prep
%autosetup -p1
%build
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
%{_libdir}/cmake/

%changelog
*   Sun Jun 19 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.29-4
-   Bump version as a part of libxslt upgrade
*   Mon Jan 24 2022 Ankit Jain <ankitja@vmware.com> 1.29-3
-   Version Bump to build with new version of cmake
*   Wed Oct 06 2021 Tapas Kundu <tkundu@vmware.com> 1.29-2
-   Fix build with updated python symlink changes
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
