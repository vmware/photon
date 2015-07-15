Summary:	Program to generate documenation
Name:		gtk-doc
Version:	1.21
Release:	2%{?dist}
License:	GPLv2+
URL:		http://www.gnu.org/software/%{name}
Source0:	http://ftp.gnome.org/pub/gnome/sources/gtk-doc/1.21/%{name}-%{version}.tar.xz
%define sha1 gtk-doc=49b4fc9d4cf618c53f39f35f4cf2fc27b7b3dae4
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
BuildRequires:	cmake
BuildRequires:	check
BuildRequires:	python2
BuildRequires:	python2-libs
Requires:	python2
Provides:	perl(gtkdoc-common.pl)
%description
The GTK-Doc package contains a code documenter. This is useful for extracting 
specially formatted comments from the code to create API documentation. 
%prep
%setup -q
%build
./configure --prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} sysconfdir=%{_sysconfdir} datadir=%{_datadir} install
%files
%defattr(-,root,root)
%{_bindir}/*
/usr/share/*
%changelog
*   Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 1.21.1-2
-   Updated group.
*	Mon Nov 24 2014 Divya Thaluru <dthaluru@vmware.com> 1.21-1
-	Initial build. First version
