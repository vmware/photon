Summary:        X11 font utilities.
Name:           font-util
Version:        1.3.3
Release:        2%{?dist}
URL:            http://www.x.org/
Group:          Development/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://ftp.x.org/pub/individual/font/%{name}-%{version}.tar.gz
%define sha512  font-util=332a53facd1c37ed8b72195e6fac016f656484583a4bb9dc8a0e7109a30342f2bfd3b756343737982ae65abd60f5272e2b6b4af72ab8a23b14817ae0d6649776

Source1: license.txt
%include %{SOURCE1}

%description
The Xorg font utilities.

%package        devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_bindir}/*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/
%{_datadir}/*

%changelog
*   Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 1.3.3-2
-   Release bump for SRP compliance
*   Thu Dec 15 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.3-1
-   Automatic Version Bump
*   Thu Oct 20 2022 Shivani Agarwal <shivania2@vmware.com> 1.3.2-1
-   Upgrade version to 1.3.2
*   Wed May 20 2015 Alexey Makhalov <amakhalov@vmware.com> 1.3.1-1
-   initial version
