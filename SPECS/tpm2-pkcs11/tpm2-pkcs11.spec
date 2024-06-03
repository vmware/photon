Summary:        OSS implementation of the TCG TPM2 Software Stack (TSS2)
Name:           tpm2-pkcs11
Version:        1.9.0
Release:        1%{?dist}
License:        BSD 2-Clause
URL:            https://github.com/tpm2-software/tpm2-pkcs11
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/tpm2-software/tpm2-pkcs11/releases/download/1.6.0/%{name}-%{version}.tar.gz
%define sha512 tpm2=e88e78790a8d4d5a67713855106860e90dd18da00dc738ca7bfebf7979cdde54ce5089d0be015e7a208117bf393db700ca7739986c5e8138ee0e3b37344614b0

BuildRequires:  openssl-devel
BuildRequires:  tpm2-tools
BuildRequires:  tpm2-tss-devel
BuildRequires:  tpm2-abrmd-devel
BuildRequires:  libyaml-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  sqlite-devel
BuildRequires:  autoconf-archive
BuildRequires:  python3-devel
BuildRequires:  python3-cryptography
BuildRequires:  python3-setuptools
BuildRequires:  python3-PyYAML
BuildRequires:  python3-pyasn1-modules
BuildRequires:  cmocka-devel
BuildRequires:  dbus
BuildRequires:  tpm2-pytss
BuildRequires:  python3-wheel
BuildRequires:  python3-pip

Requires:   openssl
Requires:   tpm2-tools
Requires:   tpm2-tss
Requires:   tpm2-abrmd
Requires:   libyaml
Requires:   sqlite-libs
Requires:   tpm2-pytss >= 2.2.1-1

%description
OSS implementation of the TCG TPM2 PKCSv11 Software Stack

%package          tools
Summary:          The tools required to setup and configure TPM2 for PKCSv11
Requires:         %{name} = %{version}-%{release}
Requires:         python3
Requires:         python3-cryptography
Requires:         python3-setuptools
Requires:         python3-pyasn1-modules
Requires:         python3-PyYAML

%description tools
Tools for TCG TPM2 PKCSv11 Software Stack

%prep
%autosetup -p1

%build
autoreconf -vif

%configure \
  --enable-unit

%make_build PACKAGE_VERSION=%{version}

cd tools
%pyproject_wheel

%install
%make_install %{?_smp_mflags}

rm %{buildroot}%{_libdir}/pkgconfig/tpm2-pkcs11.pc

cd tools
%pyproject_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
%make_build check
cd tools
python3 setup.py test

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/libtpm2_pkcs11.so
%{_libdir}/libtpm2_pkcs11.so.0*

%files tools
%defattr(-,root,root,-)
%{_bindir}/tpm2_ptool
%{python3_sitelib}/*

%changelog
* Mon Jun 03 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.9.0-1
- Upgrade to v1.9.0
* Thu Mar 07 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.0-7
- Bump version as a part of dbus upgrade
* Mon Mar 04 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.8.0-6
- Bump version as a part of sqlite upgrade to v3.43.2
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.8.0-5
- Bump version as a part of openssl upgrade
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 1.8.0-4
- bump release as part of sqlite update
* Tue Dec 06 2022 Prashant S Chauhan <psinghchauha@vmware.com> 1.8.0-3
- Update release to compile with python 3.11
* Sun Nov 13 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.8.0-2
- Bump version as a part of autoconf-archive upgrade
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com>  1.8.0-1
- Upgrade to v1.8.0
* Sat Jul 30 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.6.0-4
- Bump version as a part of sqlite upgrade
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.6.0-3
- Fix cmocka dependency
* Thu Sep 02 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.6.0-2
- openssl 3.0.0 compatibility
* Sun Aug 8 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.6.0-1
- Initial build. First version
