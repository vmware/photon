Summary:      A secure password manager for unix systems.
Name:         password-store
Version:      1.7.4
Release:      1%{?dist}
License:      GPLv2
URL:          https://www.passwordstore.org/
Group:        System Environment/Development
Vendor:       VMware, Inc.
Distribution: Photon
Source0:      https://git.zx2c4.com/password-store/snapshot/%{name}-%{version}.tar.xz
%define sha1  password-store=01ce4a6b855f617643e74b2b2398cde4e89e6d03
BuildArch:    noarch
Requires:     tree
Requires:     gnupg

%description
Password management should be simple and follow Unix philosophy. With pass,
each password lives inside of a gpg encrypted file whose filename is the title
of the website or resource that requires the password. These encrypted files
may be organized into meaningful folder hierarchies, copied from computer to
computer, and, in general, manipulated using standard command line file
management utilities.

%prep
%setup -q

%build
# nothing to build. Only shell scripts.

%install
rm -rf %{buildroot}%{_infodir}
make DESTDIR=%{buildroot} install

%check
make test

%files
%license COPYING
/usr/bin/pass
/usr/share/bash-completion/completions/pass
%{_mandir}/man1/*

%changelog
*   Mon Oct 11 2021 Nitesh Kumar <kunitesh@vmware.com> 1.7.4-1
-   Version Upgrade to fix CVE-2020-28086.
*   Fri Feb 28 2020 Siddharth Chandrasekaran <csiddharth@vmware.com> 1.7.3-2
-   Add tree and gnupg as required packages for password-store
*   Mon Sep 23 2019 Siddharth Chandrasekaran <csiddharth@vmware.com> 1.7.3-1
-   Add package password-store v1.7.3 to PhotonOS
