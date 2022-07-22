Summary:          OSS implementation of the TCG TPM2 Software Stack (TSS2)
Name:             tpm2-tss
Version:          3.2.0
Release:          1%{?dist}
License:          BSD 2-Clause
URL:              https://github.com/tpm2-software/tpm2-tss
Group:            System Environment/Security
Vendor:           VMware, Inc.
Distribution:     Photon
Source0:          %{name}-%{version}.tar.gz
%define sha512    tpm2-tss=cabb411f074dfa94919ba914849aac77a0ac2f50622e28a1406cf575369148774748e0e2b7a7c566ec83561a96d4b883bac5a3b1763f4cf48668a0c5d68c0a23
BuildRequires:    openssl-devel shadow
Requires:         openssl
%description
OSS implementation of the TCG TPM2 Software Stack (TSS2)

%package devel
Summary:      The libraries and header files needed for TSS2 development.
Requires:     %{name} = %{version}-%{release}
%description  devel
The libraries and header files needed for TSS2 development.

%prep
%autosetup
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
if [ $1 -eq 0 ]; then
    # this is delete operation
    if getent passwd tss >/dev/null; then
        userdel tss
    fi
    if getent group tss >/dev/null; then
        groupdel tss
    fi
fi

%files
%defattr(-,root,root)
%{_sysconfdir}/udev/rules.d/tpm-udev.rules
%{_libdir}/*.so.0.0.0
%{_libdir}/*.so.1.0.0

%files devel
%defattr(-,root,root)
%{_includedir}/tss2/*
%{_libdir}/pkgconfig/*
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/*.so.0
%{_libdir}/*.so.1
%{_mandir}/man3
%{_mandir}/man7

%changelog
*   Wed Jul 20 2022 Shivani Agarwal <shivania2@vmware.com> 3.2.0-1
-   Upgrade version to 3.2.0
-   Support for openssl 3.0.0
*   Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.1-3
-   Bump up release for openssl
*   Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.0.1-2
-   openssl 1.1.1
*   Wed Sep 23 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0.1-1
-   Automatic Version Bump
*   Wed Aug 12 2020 Gerrit Photon <photon-checkins@vmware.com> 3.0.0-1
-   Automatic Version Bump
*   Fri Jul 24 2020 Gerrit Photon <photon-checkins@vmware.com> 2.4.1-1
-   Automatic Version Bump
*   Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 2.2.0-1
-   Initial build. First version
