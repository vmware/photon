Summary:	Tool for managing dbx updates installed on a machine.
Name:		dbxtool
Version:	8
Release:	1%{?dist}
License:	GPLv2
URL:		https://github.com/rhboot/dbxtool
Group:		System Environment/System Utilities
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/rhboot/dbxtool/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
%define sha1 dbxtool=61da2c3e4ea3411e6379a671b09c14eae6954fe6
Patch0:         0001-dbxtool-Don-t-apply-unless-force-if-PK-or-KEK-are-un.patch
Patch1:         0003-Treat-dbxtool-a-dir-with-an-empty-directory-correctl.patch
Patch2:         0006-fix-relop-in-esl_iter_next.patch
BuildRequires:	popt-devel efivar-devel
Requires:	efivar
%description
Tool for managing dbx updates installed on a machine.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%build
make %{?_smp_mflags} PREFIX=%{_prefix} LIBDIR=%{_libdir}
%install
make INSTALLROOT=%{buildroot} \
    PREFIX=%{_prefix} \
    LIBDIR=%{_libdir} \
    install
rm -rf %{buildroot}/etc
rm %{buildroot}/%{_datadir}/%{name}/DBXUpdate-2016-08-09-13-16-00.bin

%check
make %{?_smp_mflags} test

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/%{name}
/usr/lib/systemd/system/%{name}.service
%{_docdir}/%{name}/COPYING
%{_mandir}/man1/%{name}.1.gz

%changelog
*   Wed Jul 29 2020 Alexey Makhalov <amakhalov@vmware.com> 8-1
-   Initial build. First version
