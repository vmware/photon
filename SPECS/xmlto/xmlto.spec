Summary:    The  purpose  of  xmlto is to convert an XML file to the desired format
Name:       xmlto
Version:    0.0.28
Release:    2%{?dist}
License:    GPLv2+
URL:        https://pagure.io/xmlto
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution: Photon
Source0:     http://releases.pagure.org/xmlto/%{name}-%{version}.tar.gz
%define sha1 xmlto=235feb4d2aeccf7467f458a3e18b20445f89cc0f
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
%setup -q

%build
%configure

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*/*
%{_datadir}/xmlto/*

%changelog
*   Tue Jan 05 2021 Shreenidhi Shedi <sshedi@vmware.com> 0.0.28-2
-   Fix build with new rpm
*   Thu Apr 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.0.28-1
-   Initial build.  First version
