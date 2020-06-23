Summary:        Shell script to auto detect free size on disk and grow partition.
Name:           cloud-utils
Version:        0.31
Release:        1%{?dist}
License:        GPLv3
Group:          System Environment
Source0:        https://launchpad.net/cloud-utils/trunk/%{version}/+download/cloud-utils-%{version}.tar.gz
URL:            https://launchpad.net/cloud-utils
Vendor:         VMware Inc
Distribution:   Photon
Requires:       gptfdisk
Requires:       gawk
Requires:       (util-linux or toybox)
BuildArch:      noarch

%define sha1 cloud-utils=44ef173f0753bb28be970fdfc5a5a5a352c25ce0

%description
Cloud-utils brings in growpart script. This script is very useful for
detecting available disk size and grow the partition.
This is generally used by cloud-init for disk space manangement on cloud images.

%prep
%setup -q -n cloud-utils-%{version}

%build
%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
cp bin/growpart $RPM_BUILD_ROOT/%{_bindir}/
cp man/growpart.* $RPM_BUILD_ROOT/%{_mandir}/man1/

%files
%{_bindir}/growpart
%doc %{_mandir}/man1/growpart.*

%changelog
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 0.31-1
-   Automatic Version Bump
*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 0.30-3
-   Requires util-linux or toybox
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.30-2
-   Fix arch
*   Wed Mar 29 2017 Kumar Kaushik <kaushikk@vmware.com> 0.30-1
-   Initial build.  First version
