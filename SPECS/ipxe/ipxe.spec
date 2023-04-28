%global security_hardening none
%global commit          d2063b7693e0e35db97b2264aa987eb6341ae779
%define debug_package %{nil}

Summary:        iPXE open source boot firmware
Name:           ipxe
Version:        1.21.1
Release:        5%{?dist}
License:        GPLv2
URL:            http://ipxe.org
Group:          System Environment/Daemons
Vendor:         VMware, Inc.
Distribution:   Photon

#Download URL:  https://github.com/ipxe/ipxe/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha512  %{name}=47400975110ed4ab95835aa1b7c8d5a6917c19c5713c6ab88bc0741a3adcd62245a9c4251d1f46fffc45289c6b18bf893f86dbc3b67d3189c41b7f198367ecaa

BuildArch:      x86_64

BuildRequires:  binutils
BuildRequires:  binutils-devel
BuildRequires:  cdrkit
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libgcc-devel
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  xz
BuildRequires:  xz-devel
BuildRequires:  zlib
BuildRequires:  zlib-devel

%description
iPXE is the leading open source network boot firmware. It provides a full
PXE implementation enhanced with additional features.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
cd src
make NO_WERROR=1 %{_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
mkdir -p %{buildroot}%{_datadir}/%{name}
install -vDm 644 src/bin/%{name}.{dsk,iso,lkrn,usb} %{buildroot}%{_datadir}/%{name}/
install -vDm 644 src/bin/*.{rom,mrom} %{buildroot}%{_datadir}/%{name}/

%files
%defattr(-,root,root)
%{_datadir}/%{name}/%{name}.dsk
%{_datadir}/%{name}/%{name}.iso
%{_datadir}/%{name}/%{name}.lkrn
%{_datadir}/%{name}/%{name}.usb
%{_datadir}/%{name}/10222000.rom
%{_datadir}/%{name}/10500940.rom
%{_datadir}/%{name}/10ec8139.rom
%{_datadir}/%{name}/15ad07b0.rom
%{_datadir}/%{name}/1af41000.rom
%{_datadir}/%{name}/8086100e.mrom
%{_datadir}/%{name}/8086100f.mrom
%{_datadir}/%{name}/808610d3.mrom
%{_datadir}/%{name}/80861209.rom
%{_datadir}/%{name}/rtl8139.rom

%changelog
*   Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.21.1-5
-   Bump version as a part of zlib upgrade
*   Fri Dec 23 2022 Oliver Kurth <okurth@vmware.com> 1.21.1-4
-   bump version as part of xz upgrade
*   Thu Nov 10 2022 Dweep Advani <dadvani@vmware.com> 1.21.1-3
-   Rebuild for perl version upgrade to 5.36.0
*   Sun Sep 18 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.21.1-2
-   Fix build with latest tool chain
*   Thu Apr 29 2021 Gerrit Photon <photon-checkins@vmware.com> 1.21.1-1
-   Automatic Version Bump
*   Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 1.20.1-2
-   GCC-10 support.
*   Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.20.1-1
-   Automatic Version Bump
*   Wed Apr 01 2020 Alexey Makhalov <amakhalov@vmware.com> 20180717-3
-   Fix compilation issue with gcc-8.4.0
*   Mon Oct 22 2018 Ajay Kaher <akaher@vmware.com> 20180717-2
-   Adding BuildArch
*   Thu Oct 11 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 20180717-1
-   Use commit date instead of commit id as the package version.
*   Wed Aug 08 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> d2063b7-1
-   Update version to get it to build with gcc 7.3
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com>  553f485-2
-   deactivate debuginfo gen
*   Mon Mar 13 2017 Alexey Makhalov <amakhalov@vmware.com> 553f485-1
-   Version update to build with gcc-6.3
-   Removed linux/linux-devel build-time dependency
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> ed0d7c4-2
-   GA - Bump release of all rpms
*   Thu Nov 12 2015 Vinay Kulkarni <kulkarniv@vmware.com> ed0d7c4-1
-   Initial build. First version
