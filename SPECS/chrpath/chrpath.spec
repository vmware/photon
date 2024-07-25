Summary:    Change rpath of binaries
Name:       chrpath
Version:    0.16
Release:    1%{?dist}
License:    GPL+
URL:        https://chrpath.alioth.debian.org/
Group:          Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon
Source0:    https://alioth.debian.org/frs/download.php/file/3979/%{name}-%{version}.tar.gz
%define sha1 chrpath=174bb38c899229f4c928734b20e730f61191795a

%description
Command line tool to adjust the RPATH or RUNPATH of ELF binaries.

%prep
%setup -q


%build
%configure
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
rm -rf %{buildroot}/usr/doc


%files
%doc AUTHORS README NEWS ChangeLog* COPYING
%{_bindir}/chrpath
%{_mandir}/man1/chrpath.1*

%changelog
*   Wed Apr 05 2017 Anish Swaminathan <anishs@vmware.com> 0.16-1
-   Initial packaging
