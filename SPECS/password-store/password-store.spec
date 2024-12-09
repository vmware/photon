Summary:       A secure password manager for unix systems.
Name:          password-store
Version:       1.7.4
Release:       3%{?dist}
URL:           https://www.passwordstore.org/
Group:         System Environment/Development
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       https://git.zx2c4.com/password-store/snapshot/%{name}-%{version}.tar.xz
%define sha512 password-store=1fe108895b224451b54e545d399b6a97040e094049448509f92ae33164a5cf9044a91f52edfc705fcf333f6526df1a478deeebc4df109764d58100f9e3e22681

Source1: license.txt
%include %{SOURCE1}
BuildArch:     noarch
Requires:      tree
Requires:      gnupg

%description
Password management should be simple and follow Unix philosophy. With pass,
each password lives inside of a gpg encrypted file whose filename is the title
of the website or resource that requires the password. These encrypted files
may be organized into meaningful folder hierarchies, copied from computer to
computer, and, in general, manipulated using standard command line file
management utilities.

%prep
%autosetup

%build
# nothing to build. Only shell scripts.

%install
rm -rf %{buildroot}%{_infodir}
make DESTDIR=%{buildroot} install %{?_smp_mflags}

%check
make test %{?_smp_mflags}

%files
%license COPYING
/usr/bin/pass
/usr/share/bash-completion/completions/pass
%{_mandir}/man1/*

%changelog
*   Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.7.4-3
-   Release bump for SRP compliance
*   Tue May 23 2023 Shivani Agarwal <shivania2@vmware.com> 1.7.4-2
-   Bump up version to compile with new gnupg
*   Mon Oct 11 2021 Nitesh Kumar <kunitesh@vmware.com> 1.7.4-1
-   Version Upgrade to fix CVE-2020-28086.
*   Fri Feb 28 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 1.7.3-2
-   Add tree and gnupg as required packages for password-store
*   Mon Sep 23 2019 Siddharth Chandrasekaran <csiddharth@vmware.com> 1.7.3-1
-   Add package password-store v1.7.3 to PhotonOS
