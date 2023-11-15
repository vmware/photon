Summary:          OSS implementation of the TCG TPM2 Software Stack (TSS2)
Name:             tpm2-tss
Version:          2.4.5
Release:          3%{?dist}
License:          BSD 2-Clause
URL:              https://github.com/tpm2-software/tpm2-tss
Group:            System Environment/Security
Vendor:           VMware, Inc.
Distribution:     Photon
Source0:          %{name}-%{version}.tar.gz
%define sha512 tpm2=2c92af07ed1cc3665c19479c00ce5608883081f311192a264a4f7d9119c75ac582596c53b910534c4b66dbb60de2ffd3d6218169748332609c2e0fc89f519259
Patch0:           0001-Fix-cflags-for-tss2.patch
BuildRequires:    openssl-devel
Requires:         openssl
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun): /usr/sbin/userdel /usr/sbin/groupdel
%description
OSS implementation of the TCG TPM2 Software Stack (TSS2)

%package devel
Summary:     The libraries and header files needed for TSS2 development.
Requires:    %{name} = %{version}-%{release}
%description devel
The libraries and header files needed for TSS2 development.

%prep
%autosetup -p1

%build
%configure \
    --disable-static \
    --disable-doxygen-doc \
    --enable-fapi=no \
    --with-udevrulesdir=/etc/udev/rules.d
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}

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
%{_libdir}/*.so.0
%{_libdir}/*.so.0.0.0

%files devel
%defattr(-,root,root)
%{_includedir}/tss2/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_mandir}/man3
%{_mandir}/man7

%changelog
* Mon Nov 20 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 2.4.5-3
- Fix include dir in pkgconfig
* Mon Oct 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.4.5-2
- Remove .la files
* Mon Dec 14 2020 Gerrit Photon <photon-checkins@vmware.com> 2.4.5-1
- Automatic Version Bump
* Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.4.1-1
- Update version to 2.4.1 since tpm-tools update to 4.1.3
* Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.2.0-1
- Initial build. First version
