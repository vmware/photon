Summary:    Modular initramfs image creation utility
Name:       mkinitcpio
Version:    19
Release:    3%{?dist}
License:    GPLv2
URL:        https://projects.archlinux.org/mkinitcpio.git/
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    https://projects.archlinux.org/mkinitcpio.git/snapshot/%{name}-%{version}.tar.gz
%define sha1 mkinitcpio=3fef28312965d7cc254b6ac1ea38be16dcb46bf9
BuildRequires: asciidoc
BuildRequires: python2-libs
BuildRequires: python-xml
BuildRequires: docbook-xsl
BuildRequires: libxml2-devel
BuildRequires: libxslt
BuildArch:     noarch

%description
Multi-format archive and compression library

%prep
%setup -q

%build

for i in "hooks/*" ; do sed -i "s/\#\!\/usr\/bin\/ash/\#\!\/bin\/bash/" $i; done
sed -i "s/\#\!\/usr\/bin\/ash/\#\!\/bin\/bash/" init
sed -i "s/\#\!\/usr\/bin\/ash/\#\!\/bin\/bash/" shutdown
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
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 19-3
-   Fix arch
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 19-2
-	GA - Bump release of all rpms
*   Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 19-1
-   Updated to new version.
*   Sat Jul 11 2015 Touseef Liaqat <tliaqat@vmware.com> 18-2
-   Remove ash dependency
*   Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 18-1
-   Initial build.  First version
