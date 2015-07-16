Summary:	Program shows full path of (shell) commands
Name:		which
Version:	2.20
Release:	1%{?dist}
License:	GPLv3+
URL:		http://savannah.gnu.org/projects/which
Source0:	http://ftp.gnu.org/gnu/which/%{name}-%{version}.tar.gz
%define sha1 which=3bcd6d87aa5231917ba7123319eedcae90cfa0fd
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution: Photon
%description
Program for showing the full the path of (shell) commands.
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%files
%defattr(-,root,root)
%{_bindir}/*
/usr/share/info/*
%{_mandir}/man1/*
%changelog
*	Wed Oct 21 2014 Divya Thaluru <dthaluru@vmware.com> 2.20-1
-	Initial build. First version
