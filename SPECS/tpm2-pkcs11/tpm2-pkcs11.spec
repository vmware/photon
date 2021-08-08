%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:          OSS implementation of the TCG TPM2 Software Stack (TSS2)
Name:             tpm2-pkcs11
Version:          1.6.0
Release:          1%{?dist}
License:          BSD 2-Clause
URL:              https://github.com/tpm2-software/tpm2-pkcs11
Group:            System Environment/Security
Vendor:           VMware, Inc.
Distribution:     Photon
Source0:          %{name}-%{version}.tar.gz
%define sha1      tpm2=3e9e018c0f83c1351cc68ae5f3fcb5f4cf831c5f
BuildRequires:    make gcc openssl-devel tpm2-tools tpm2-tss-devel tpm2-abrmd-devel
BuildRequires:    libyaml-devel libgcrypt-devel sqlite-devel autoconf-archive
BuildRequires:    python3 python3-cryptography python3-setuptools
BuildRequires:    python3-PyYAML python3-pyasn1-modules
BuildRequires:    cmocka dbus
Requires:         openssl tpm2-tools tpm2-tss tpm2-abrmd libyaml sqlite-libs
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
%autosetup -p1 -n %{name}-%{version}
%build
./bootstrap
%configure --enable-unit
make %{?_smp_mflags} PACKAGE_VERSION=%{version}
cd tools
python3 setup.py build

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install
rm %{buildroot}%{_libdir}/pkgconfig/tpm2-pkcs11.pc
rm %{buildroot}%{_libdir}/libtpm2_pkcs11.la
cd tools
python3 setup.py install --root=%{buildroot} --optimize=1 --skip-build

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
make %{?_smp_mflags} check
cd tools
python3 setup.py test

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
*   Sun Aug 8 2021 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.6.0-1
-   Initial build. First version
