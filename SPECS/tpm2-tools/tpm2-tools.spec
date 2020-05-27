Summary:	The source repository for the TPM (Trusted Platform Module) 2 tools
Name:		tpm2-tools
Version:	3.1.3
Release:	1%{?dist}
License:	BSD 2-Clause
URL:		https://github.com/tpm2-software/tpm2-tools
Group:		System Environment/Security
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	%{name}-%{version}.tar.gz
%define sha1 tpm2=126f83d927a13aa5999769e33339136b2c7c5008
BuildRequires:	openssl-devel curl-devel tpm2-tss-devel
Requires:	openssl curl tpm2-tss
%description
The source repository for the TPM (Trusted Platform Module) 2 tools

%prep
%setup -q
%build
%configure \
    --disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1

%changelog
*   Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> 3.1.3-1
-   Initial build. First version
