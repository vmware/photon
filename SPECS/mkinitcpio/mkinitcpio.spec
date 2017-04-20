Summary:    Modular initramfs image creation utility
Name:       mkinitcpio
Version:    23
Release:    1%{?dist}
License:    GPLv2
URL:        https://projects.archlinux.org/mkinitcpio.git/
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    https://projects.archlinux.org/mkinitcpio.git/snapshot/%{name}-%{version}.tar.gz
%define sha1 mkinitcpio=4459418eb423b2699e798c4523a59cc07a567a98
BuildRequires: asciidoc
BuildRequires: python2-libs
BuildRequires: python-xml
BuildRequires: docbook-xsl
BuildRequires: libxml2-devel
BuildRequires: libxslt

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
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 23-1
-   Update package version
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 19-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 19-1
-   Updated to new version.
*   Sat Jul 11 2015 Touseef Liaqat <tliaqat@vmware.com> 18-2
-   Remove ash dependency
*   Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 18-1
-   Initial build.  First version
