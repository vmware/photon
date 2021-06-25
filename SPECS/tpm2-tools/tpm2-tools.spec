Summary:        The source repository for the TPM (Trusted Platform Module) 2 tools
Name:           tpm2-tools
Version:        4.1.3
Release:        3%{?dist}
License:        BSD 2-Clause
URL:            https://github.com/tpm2-software/tpm2-tools
Group:          System Environment/Security
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1    tpm2-tools=b2cef4d06817a6859082d50863464a858a493a63
Patch0:         tpm2-tools-CVE-2021-3565.patch
BuildRequires:  openssl-devel curl-devel tpm2-tss-devel
Requires:       openssl curl tpm2-tss
%if %{with_check}
BuildRequires:  ibmtpm
BuildRequires:  systemd
%endif
%description
The source repository for the TPM (Trusted Platform Module) 2 tools.

%prep
%setup -q
%patch0 -p1
%build
%configure \
    --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

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
*   Fri Jun 25 2021 Dweep Advani <dadvani@vmware.com> 4.1.3-3
-   Patched for CVE-2021-3565
*   Fri Jun 19 2020 Michelle Wang <michellew@vmware.com> 4.1.3-2
-   update make check with ibmtpm
*   Thu Jun 18 2020 Michelle Wang <michellew@vmware.com> 4.1.3-1
-   Update version to 4.1.3
*   Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 3.1.3-1
-   Initial build. First version
