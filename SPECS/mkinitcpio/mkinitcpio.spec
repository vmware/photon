Summary:    Modular initramfs image creation utility
Name:       mkinitcpio
Version:    28
Release:    2%{?dist}
License:    GPLv2
URL:        https://projects.archlinux.org/mkinitcpio.git
Group:      System Environment/Development
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://projects.archlinux.org/mkinitcpio.git/snapshot/%{name}-%{version}.tar.gz
%define sha512 %{name}=53f6db0507ecad1d2ee4cbc18642de9bb2443995c526d6065291547a49c8e37917e632df1b3579808f718385d2604af0e9719fb7fa6459d286993814c4ff76c8

Patch0:     mkinitcpio-shutdown-ramfs.service.patch

BuildRequires: asciidoc3
BuildRequires: git
BuildRequires: python3
BuildRequires: python3-xml
BuildRequires: docbook-xsl
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel

BuildArch:     noarch

%description
Multi-format archive and compression library

%prep
%autosetup -p0

%build

for i in "hooks/*" init shutdown; do
  sed -i "s/\#\!\/usr\/bin\/ash/\#\!\/bin\/bash/" $i
done

sed -i "s/a2x/a2x3 --verbose --no-xmllint/" Makefile

%make_build

%install
%make_install %{?_smp_mflags}

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/*
%{_bindir}/*
%{_sysconfdir}/*
%{_datadir}/*

%changelog
*   Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 28-2
-   Bump up to compile with python 3.10
*   Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 28-1
-   Automatic Version Bump
*   Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 24-3
-   Build with python3
-   Mass removal python2
*   Fri Jan 18 2019 Alexey Makhalov <amakhalov@vmware.com> 24-2
-   Added buildRequires python2.
*   Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 24-1
-   Update to version 24
*   Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 23-3
-   fix directory create in shutdown service
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 23-2
-   Fix arch
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
