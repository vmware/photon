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
%define sha512 xmlto=b4de619c840ed9329aed15e6a2bcd830864c250cd134474aeb157571019fa443835e17f68851d35971f775ba5e5c65c61429cf0616c7839cdc51e83f80916a80
BuildRequires:    docbook-xsl
BuildRequires:    docbook-xml
BuildRequires:    libxslt-devel
Requires:         systemd
Requires:	  docbook-xsl
Requires:	  libxslt

%description
The  purpose  of  xmlto is to convert an XML file to the desired format

%prep
%autosetup -p1

%build
%configure

make %{?_smp_mflags}

%install
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

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
*   Sun Jun 19 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 0.0.28-2
-   Bump version as a part of libxslt upgrade
*   Thu Apr 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.0.28-1
-   Initial build.  First version
