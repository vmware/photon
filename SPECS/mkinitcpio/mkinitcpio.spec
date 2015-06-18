Summary:    Modular initramfs image creation utility
Name:       mkinitcpio
Version:    18
Release:    1
License:    GPLv2
URL:        https://projects.archlinux.org/mkinitcpio.git/
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    https://projects.archlinux.org/mkinitcpio.git/snapshot/%{name}-%{version}.tar.gz
BuildRequires: asciidoc
BuildRequires: python2-libs
BuildRequires: docbook-xsl
BuildRequires: libxml2-devel
BuildRequires: libxslt

%description
Multi-format archive and compression library

%prep
%setup -q

%build

sed -i "s/a2x/a2x --verbose --no-xmllint/" Makefile

make %{?_smp_mflags}

%install
rm -rf %{buildroot}%{_infodir}
make DESTDIR=%{buildroot} install

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/lib/*
/usr/bin/*
/etc/*
/usr/share/*

%changelog
*   Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 18-1
-   Initial build.  First version
