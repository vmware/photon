Summary:        This project is an implementation of the TCG TPM 2.0 specification.
Name:           ibmtpm
Version:        1682
Release:        2%{?dist}
URL:            https://sourceforge.net/projects/ibmswtpm2/files
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: %{name}%{version}.tar.gz
%define sha512 %{name}=564c2154e5459cbbf4ec052bea7909d1eaff0aa07b291c7de44b1204ecfda3c4156fa18da4499e4202b8772b54ae30d0c7c89bd12cd415f3882d17c8d340686d

Source1: license.txt
%include %{SOURCE1}

BuildRequires: openssl-devel
BuildRequires: systemd-devel
BuildRequires: curl-devel

Requires: openssl
Requires: curl
Requires: systemd

%description
This project is an implementation of the TCG TPM 2.0 specification.
It is based on the TPM specification Parts 3 and 4 source code donated by Microsoft,
with additional files to complete the implementation.

%prep
%autosetup -p1 -cn %{name}-%{version}

%build
cd src
GCCVERSION=$(gcc --version | grep ^gcc | sed 's/^.* //g')
$(dirname $(gcc -print-prog-name=cc1))/install-tools/mkheaders
%make_build

%install
cd src
%make_install %{?_smp_mflags}
mkdir -p %{buildroot}%{_unitdir}
cat << EOF >> %{buildroot}%{_unitdir}/ibmtpm_server.service
[Unit]
Description=ibmtpm_server

[Service]
Type=simple
ExecStart=%{_bindir}/tpm_server
EOF

%files
%defattr(-,root,root)
%{_bindir}/*
%{_unitdir}/ibmtpm_server.service

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 1682-2
- Release bump for SRP compliance
* Sun Oct 09 2022 Shreenidhi Shedi <sshedi@vmware.com> 1682-1
- Upgrade to v1682
* Thu Jun 03 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1661-2
- Compatibility with openssl 3.0
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1661-1
- Automatic Version Bump
* Thu Oct 08 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1637-3
- Fix GCC path issue
* Thu Sep 10 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1637-2
- Compatibility with openssl 1.1.1
* Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 1637-1
- Automatic Version Bump
* Fri May 29 2020 Michelle Wang <michellew@vmware.com> 1628-1
- Initial build. First version
