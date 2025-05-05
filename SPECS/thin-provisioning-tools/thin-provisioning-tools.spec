Summary:        Thin provisioning tools
Name:           thin-provisioning-tools
Version:        0.9.0
Release:        3%{?dist}
License:        GPLv3+
Group:          System Environment/Base
URL:            https://github.com/jthornber/thin-provisioning-tools
Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}=e1796fb3948847d72ca8247cae58017507c0a847a00201b93668eeb8fbfea4107c4c2affa5c211c149798a89b10474e83d2bd61a5545a668299be97aed591e0f
BuildRequires:  expat-devel, libaio-devel, boost-devel
Requires:       expat, libaio
Vendor:         VMware, Inc.
Distribution:   Photon

%description
thin-provisioning-tools contains check,dump,restore,repair,rmap
and metadata_size tools to manage device-mapper thin provisioning
target metadata devices; cache check,dump,metadata_size,restore
and repair tools to manage device-mapper cache metadata devices
are included and era check, dump, restore and invalidate to manage
snapshot eras

%prep
%autosetup -p1

%build
autoconf
export CFLAGS="%{optflags}"
export LDFLAGS=""
%configure STRIP=/bin/true

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} MANDIR=%{_mandir} install %{?_smp_mflags}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING README.md
%{_mandir}/man8/*
%{_sbindir}/*

%changelog
*   Mon May 05 2025 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.9.0-3
-   Version bump for expat upgrade
*   Thu Feb 29 2024 Anmol Jain <anmol.jain@broadcom.com> 0.9.0-2
-   Bump version as a part of expat upgrade
*   Wed Sep 02 2020 Gerrit Photon <photon-checkins@vmware.com> 0.9.0-1
-   Automatic Version Bump
*   Wed Jun 10 2020 Gerrit Photon <photon-checkins@vmware.com> 0.8.5-1
-   Automatic Version Bump
*   Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 0.7.0-1
-   Update version to stable release version 0.7.0.
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.6.3-3
-   Use standard configure macros
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6.3-2
-   Ensure non empty debuginfo
*   Tue Mar 28 2017 Xiaolin Li <xiaolinl@vmware.com> 0.6.3-1
-   Updated to version 0.6.3.
*   Mon Mar 13 2017 Alexey Makhalov <amakhalov@vmware.com> 0.6.1-3
-   Fix gcc-6.3 compilation errors
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.6.1-2
-   GA - Bump release of all rpms
*   Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> 0.6.1-1
-   Updating version
*   Tue Mar 3 2015 Divya Thaluru <dthaluru@vmware.com> 0.4.1-1
-   Initial version
