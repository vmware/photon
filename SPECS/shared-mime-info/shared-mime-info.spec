Summary:        MIME database
Name:           shared-mime-info
Version:        2.2
Release:        5%{?dist}
URL:            http://freedesktop.org
Group:          Applications/Internet
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://freedesktop.org/~hadess/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

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
* Wed Jan 22 2025 Tapas Kundu <tapas.kundu@broadcom.com> 2.2-5
- Bump version as a part of meson upgrade
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.2-4
- Release bump for SRP compliance
* Thu May 25 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.2-3
- Bump version as a part of libxml2 upgrade
* Sat Jan 14 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.2-2
- Bump version as a part of gettext upgrade
* Mon Aug 22 2022 Shivani Agarwal <shivania2@vmware.com> 2.2-1
- Upgrade to version 2.2
* Wed Jun 3 2015 Alexey Makhalov <amakhalov@vmware.com> 1.4-1
- initial version
