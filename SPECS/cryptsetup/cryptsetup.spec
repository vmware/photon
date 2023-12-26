Summary:        Utility to setup encrypted disks
Name:           cryptsetup
Version:        2.4.2
Release:        3%{?dist}
License:        GPLv2+ and LGPLv2+
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://gitlab.com/cryptsetup/cryptsetup

Source0: %{name}-v%{version}.tar.gz
%define sha512 %{name}=19fcc155388207f3fb03d57c415467d0062361be787899595a053cf1d3564aad68ed306480c6bb85e525fa56729c0397348f35c51f82b02712693154df2115ff

Patch0: CVE-2021-4122.patch

BuildRequires: systemd-devel
BuildRequires: openssl-devel
BuildRequires: popt-devel
BuildRequires: device-mapper-devel
BuildRequires: gcc
BuildRequires: make
BuildRequires: json-c-devel
BuildRequires: libpwquality-devel
BuildRequires: libargon2-devel
BuildRequires: libssh-devel

Requires: cryptsetup-libs = %{version}-%{release}
Requires: libpwquality
Requires: util-linux-libs
Requires: openssl
Requires: device-mapper-libs

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

%package -n     %{name}-ssh-token
Summary:        Cryptsetup LUKS2 SSH token
Requires:       %{name}-libs = %{version}-%{release}
Requires:       libssh

%description ssh-token
This package contains the LUKS2 SSH token.

%prep
%autosetup -p1 -n %{name}-v%{version}

%build
bash ./autogen.sh
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

%files ssh-token
%license COPYING COPYING.LGPL
%{_libdir}/%{name}/libcryptsetup-token-ssh.so
%{_mandir}/man8/cryptsetup-ssh.8.gz
%{_sbindir}/cryptsetup-ssh
%exclude %{_libdir}/%{name}/libcryptsetup-token-ssh.la

%changelog
* Tue Dec 26 2023 Mukul Sikka <msikka@vmware.com> 2.4.2-3
- Version bump up to use libssh v0.9.8
* Tue Sep 05 2023 Nitesh Kumar <kunitesh@vmware.com> 2.4.2-2
- Version bump up to use libssh v0.9.7
* Wed Jan 12 2022 Tapas Kundu <tkundu@vmware.com> 2.4.2-1
- Fix CVE-2021-4122
- Update to 2.4.2
* Thu Apr 8 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.3.5-1
- Initial package
