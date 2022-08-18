Summary:    OSS implementation of the TCG TPM2 Software Stack (TSS2)
Name:       tpm2-tss
Version:    3.2.0
Release:    3%{?dist}
License:    BSD 2-Clause
URL:        https://github.com/tpm2-software/tpm2-tss
Group:      System Environment/Security
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/tpm2-software/tpm2-tss/releases/download/3.2.0/%{name}-%{version}.tar.gz
%define sha512 %{name}=cabb411f074dfa94919ba914849aac77a0ac2f50622e28a1406cf575369148774748e0e2b7a7c566ec83561a96d4b883bac5a3b1763f4cf48668a0c5d68c0a23

BuildRequires:  openssl-devel
BuildRequires:  shadow

Requires: openssl

%description
OSS implementation of the TCG TPM2 Software Stack (TSS2)

%package      devel
Summary:      The libraries and header files needed for TSS2 development.
Requires:     %{name} = %{version}-%{release}

%description    devel
The libraries and header files needed for TSS2 development.

%prep
%autosetup -p1

%build
%configure \
  --disable-static \
  --disable-doxygen-doc \
  --enable-fapi=no \
  --with-udevrulesdir=%{_sysconfdir}/udev/rules.d

%make_build

%install
%make_install %{?_smp_mflags}

%post
/sbin/ldconfig
mkdir -p /var/lib/tpm
if [ $1 -eq 1 ]; then
  # this is initial installation
  if ! getent group tss >/dev/null; then
    groupadd tss
  fi
  if ! getent passwd tss >/dev/null; then
    useradd -c "TCG Software Stack" -d /var/lib/tpm -g tss \
      -s /bin/false tss
  fi
fi

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_sysconfdir}/udev/rules.d/tpm-udev.rules
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/tss2/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_mandir}/man3
%{_mandir}/man7

%changelog
* Wed Oct 05 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.2.0-3
- Fix library files packaging
* Sun Aug 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.2.0-2
- Remove .la files
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2.0-1
- Automatic Version Bump
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.3-2
- Bump up release for openssl
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.0.3-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.1-2
- openssl 1.1.1
* Wed Sep 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0.1-1
- Automatic Version Bump
* Wed Aug 12 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0.0-1
- Automatic Version Bump
* Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.4.1-1
- Automatic Version Bump
* Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.2.0-1
- Initial build. First version.
