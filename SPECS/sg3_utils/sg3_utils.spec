Summary:	Tools and Utilities for interaction with SCSI devices.
Name:		sg3_utils
Version:	1.42
Release:	2%{?dist}
License:	GPLv2
URL:		http://sg.danny.cz/sg/sg3_utils.html
Source0:	http://sg.danny.cz/sg/p/sg3_utils-1.42.tar.xz
%define sha1 sg3_utils=7af36a62d10e2f078b5c96b18e5e3f4f6143f648
Group:		System/Tools.
Vendor:		VMware, Inc.
Distribution:   Photon
Provides:       sg_utils.

%description
Linux tools and utilities to send commands to SCSI devices.

%package -n libsg3_utils-devel
Summary:        Devel pacjage for sg3_utils.
Group:          Development/Library.

%description -n libsg3_utils-devel
Package containing static library object for development.

%prep
%setup -q

%build
%configure

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -m 755 scripts/scsi_logging_level %{buildroot}/%{_bindir}
install -m 755 scripts/rescan-scsi-bus.sh %{buildroot}/%{_bindir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/*
%{_libdir}/libsgutils2.so.*

%files -n libsg3_utils-devel
%defattr(-,root,root)
%{_libdir}/libsgutils2.a
%{_libdir}/libsgutils2.la
%{_libdir}/libsgutils2.so
%{_includedir}/scsi/*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.42-2
-	GA - Bump release of all rpms
*	Thu Apr 14 2016 Kumar Kaushik <kaushikk@vmware.com> 1.42-1
-	Initial build. First version
