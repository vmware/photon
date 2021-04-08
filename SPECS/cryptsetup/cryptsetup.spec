Summary:        Utility to setup encrypted disks
Name:           cryptsetup
Version:        2.3.5
Release:        1%{?dist}
License:        GPLv2+ and LGPLv2+
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.xz
%define sha1    cryptsetup=800fc375b514c4c4cd4f2dcbff7cf413db2ba81c
URL:            https://gitlab.com/cryptsetup/cryptsetup
BuildRequires:  systemd-devel
BuildRequires:  openssl-devel
BuildRequires:  popt-devel
BuildRequires:  device-mapper-devel
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  json-c-devel
BuildRequires:  libpwquality-devel
BuildRequires:  libargon2-devel
Requires:       cryptsetup-libs = %{version}-%{release}
Requires:       libpwquality
Requires:       util-linux-libs
Requires:       openssl
Requires:       device-mapper-libs

%description
Cryptsetup is a utility used to conveniently set up disk encryption based
on the DMCrypt kernel module.

%package -n     %{name}-devel
Summary:        Headers and Libraries for Cryptsetup
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}

%description -n %{name}-devel
Headers and Libraries for integrating with Cryptsetup

%package -n     %{name}-libs
Summary:        Shared Libraries for Cryptsetup
Group:          Development/Libraries
Requires:       util-linux-libs
Requires:       libargon2
Requires:       json-c
Requires:       openssl
Requires:       device-mapper-libs

%description -n %{name}-libs
Shared libraries for Cryptsetup

%package -n     veritysetup
Summary:        Utility to set up dm-verity volumes
Requires:       %{name}-libs = %{version}-%{release}


%description -n veritysetup
Utility to set up dm-verity volumes.

%package -n     integritysetup
Summary:        Utility to set up dm-integrity volumes
Requires:       %{name}-libs = %{version}-%{release}

%description -n integritysetup
Utility to set up dm-integrity volumes.

%package -n     %{name}-reencrypt
Summary:        Utility to perform offline reencryption of LUKS enabled disks
Requires:       %{name}-libs = %{version}-%{release}

%description -n %{name}-reencrypt
Utility to perform offline reencryption of LUKS enabled disks.

%prep
%setup -q

%build
%configure --enable-fips --enable-pwquality --enable-libargon2
%make_build

%install
%make_install
rm -rf %{buildroot}%{_libdir}/*.la

%find_lang %{name}

%post -n %{name}-libs
/sbin/ldconfig

%postun -n %{name}-libs
/sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%doc AUTHORS FAQ docs/*ReleaseNotes
%{_mandir}/man8/cryptsetup.8.gz
%{_sbindir}/cryptsetup

%files -n veritysetup
%defattr(-,root,root)
%license COPYING
%{_mandir}/man8/veritysetup.8.gz
%{_sbindir}/veritysetup

%files -n integritysetup
%defattr(-,root,root)
%license COPYING
%{_mandir}/man8/integritysetup.8.gz
%{_sbindir}/integritysetup

%files reencrypt
%defattr(-,root,root)
%license COPYING
%doc misc/dracut_90reencrypt
%{_mandir}/man8/%{name}-reencrypt.8.gz
%{_sbindir}/%{name}-reencrypt

%files devel
%defattr(-,root,root)
%doc docs/examples/*
%{_includedir}/libcryptsetup.h
%{_libdir}/libcryptsetup.so
%{_libdir}/pkgconfig/libcryptsetup.pc

%files libs -f cryptsetup.lang
%defattr(-,root,root)
%license COPYING COPYING.LGPL
%{_libdir}/libcryptsetup.so.*
%{_tmpfilesdir}/cryptsetup.conf
%ghost %attr(700, -, -) %dir /run/cryptsetup

%changelog
*   Thu Apr 8 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.3.5-1
-   Initial package
