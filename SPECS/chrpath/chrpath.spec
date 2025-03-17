Summary:    Change rpath of binaries
Name:       chrpath
Version:    0.16
Release:    2%{?dist}
URL:        https://chrpath.alioth.debian.org/
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:        https://alioth.debian.org/frs/download.php/file/3979/%{name}-%{version}.tar.gz

Source1: license.txt
%include %{SOURCE1}

%description
Command line tool to adjust the RPATH or RUNPATH of ELF binaries.

%prep
%autosetup

%build
%configure
make %{?_smp_mflags}

%check
make check %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p" %{?_smp_mflags}
rm -rf %{buildroot}/usr/doc

%files
%doc AUTHORS README NEWS ChangeLog* COPYING
%{_bindir}/chrpath
%{_mandir}/man1/chrpath.1*

%changelog
*   Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 0.16-2
-   Release bump for SRP compliance
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 0.16-1
-   Initial packaging
