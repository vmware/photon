Summary:        MIME database
Name:           shared-mime-info
Version:        2.2
Release:        2%{?dist}
License:        GPLv2+
URL:            http://freedesktop.org
Group:          Applications/Internet
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://freedesktop.org/~hadess/%{name}-%{version}.tar.gz
%define sha512 %{name}=490d96daf4214ab6ac537761b67f3ff4716b95d7ea3fedd2e2ab7b0b02d946acad49790a25efcb5e949551dc4c39ba08911e59f06b198b61dcb1bc44799a2b2e

BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  intltool
BuildRequires:  glib-devel
BuildRequires:  libxml2-devel

Requires:       gettext
Requires:       glib
Requires:       libxml2

%description
The Shared Mime Info package contains a MIME database.
This allows central updates of MIME information for all supporting applications.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%ldconfig_scriptlets

%check
%meson_test

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/*

%changelog
* Sat Jan 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.2-2
- Bump version as a part of gettext upgrade
* Mon Aug 22 2022 Shivani Agarwal <shivania2@vmware.com> 2.2-1
- Upgrade to version 2.2
* Wed Jun 3 2015 Alexey Makhalov <amakhalov@vmware.com> 1.4-1
- initial version
