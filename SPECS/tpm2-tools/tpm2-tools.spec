Summary:        The source repository for the TPM (Trusted Platform Module) 2 tools
Name:           tpm2-tools
Version:        4.1.3
Release:        4%{?dist}
License:        BSD 2-Clause
URL:            https://github.com/tpm2-software/tpm2-tools
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha512    tpm2-tools=bf1ba9f8a4e12c71987650b309710574cc796e78d26c5de1cae77b0e150cea0f3b3695e56415be1994c4a6ad90e8f991d5db603138933fd21c46f7b86148a9b4
Patch0:         tpm2-tools-CVE-2021-3565.patch
Patch1:         tpm2-tools-CVE-2024-29039.patch
BuildRequires:  openssl-devel curl-devel tpm2-tss-devel
Requires:       openssl curl tpm2-tss
%if 0%{?with_check}
BuildRequires:  ibmtpm
BuildRequires:  systemd
%endif
%description
The source repository for the TPM (Trusted Platform Module) 2 tools.

%prep
%autosetup -p1

%build
%configure \
    --disable-static
%make_build

%install
%make_install

%check
if [ ! -f /dev/tpm0 ];then
   systemctl start ibmtpm_server.service
   export TPM2TOOLS_TCTI=mssim:host=localhost,port=2321
   tpm2_startup -c
   tpm2_pcrlist
fi
make %{?_smp_mflags} check

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1
/usr/share/bash-completion/*

%changelog
*   Thu Aug 01 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 4.1.3-4
-   Fix for CVE-2024-29039
*   Fri Jun 25 2021 Dweep Advani <dadvani@vmware.com> 4.1.3-3
-   Patched for CVE-2021-3565
*   Fri Jun 19 2020 Michelle Wang <michellew@vmware.com> 4.1.3-2
-   update make check with ibmtpm
*   Thu Jun 18 2020 Michelle Wang <michellew@vmware.com> 4.1.3-1
-   Update version to 4.1.3
*   Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 3.1.3-1
-   Initial build. First version
