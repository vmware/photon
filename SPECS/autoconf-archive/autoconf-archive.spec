%define debug_package %{nil}

Summary:	Autoconf macro archive
Name:		autoconf-archive
Version:	2021.02.19
Release:	1%{?dist}
License:	GPLv3+
URL:		http://www.gnu.org/software/autoconf-archive
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
%define sha1 autoconf-archive=2da40e4eebfced5f5f714dfba77f6cc3461660f8

BuildArch:  noarch
Requires:	autoconf

%description
The package contains programs for producing shell scripts that can
automatically configure source code.
%prep
%setup -q
%build
%configure
make
%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm -rf %{buildroot}%{_infodir}
# doc and license files are installed elsewhere
rm -frv %{buildroot}%{_docdir}/%{name}

%files
%doc AUTHORS NEWS README TODO
%license COPYING*
%{_datadir}/aclocal/*.m4

%changelog
*   Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 2021.02.19-1
-   Automatic Version Bump
*   Wed Jul 22 2020 Gerrit Photon <photon-checkins@vmware.com> 2019.01.06-1
-   Automatic Version Bump
*   Mon Sep 10 2018 Anish Swaminathan <anishs@vmware.com> 2018.03.13-1
-   Initial build
