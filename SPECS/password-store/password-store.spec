Summary:      A secure password manager for unix systems.
Name:         password-store
Version:      1.7.3
Release:      1%{?dist}
License:      GPLv2
URL:          https://www.passwordstore.org/
Group:        System Environment/Development
Vendor:       VMware, Inc.
Distribution: Photon
Source0:      https://git.zx2c4.com/password-store/snapshot/%{name}-%{version}.tar.xz
%define sha1  password-store=20c5442b55ae6b3b083155defc3f63b267bcaadd
BuildArch:    noarch

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
*   Mon Sep 23 2019 Siddharth Chandrasekaran <csiddharth@vmware.com> 1.7.3-1
-   Add package password-store v1.7.3 to PhotonOS
