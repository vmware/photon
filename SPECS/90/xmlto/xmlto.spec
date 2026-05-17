%global build_if %{photon_subrelease} <= 90

Summary:    The  purpose  of  xmlto is to convert an XML file to the desired format
Name:       xmlto
Version:    0.0.28
Release:    5.1.1%{?dist}
URL:        https://pagure.io/xmlto
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution: Photon

Source0: http://releases.pagure.org/xmlto/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

BuildRequires:    docbook-xsl
BuildRequires:    docbook-xml
BuildRequires:    libxslt-devel
BuildRequires:    libgcrypt-devel

Requires:   libgcrypt
Requires:   systemd
Requires:   docbook-xsl
Requires:   libxslt

%description
The  purpose  of  xmlto is to convert an XML file to the desired format

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%{_datadir}/%{name}/*

%changelog
* Fri May 15 2026 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 0.0.28-5.1.1
- Adjusted to build for subrelease 90
* Tue Mar 31 2026 Ankit Jain <ankit-aj.jain@broadcom.com> 0.0.28-5.1
- Bump after moving to SPECS/91
* Thu Dec 12 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 0.0.28-5
- Release bump for SRP compliance
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 0.0.28-4
- Bump version as a part of libxslt upgrade
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 0.0.28-3
- Bump version as a part of libxslt upgrade
* Tue Jan 05 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.0.28-2
- Fix build with new rpm
* Thu Apr 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.0.28-1
- Initial build. First version
