Summary:	Linux Key Management Utilities
Name:		keyutils
Version:	1.6.1
Release:	1%{?dist}
License:	GPL-2.0+ and LGPL-2.1+
URL:		http://people.redhat.com/~dhowells/keyutils/
Source0:	http://people.redhat.com/~dhowells/keyutils/keyutils-%{version}.tar.bz2
%define sha1 keyutils=79fb86ea60de1207183ecd0c3a038380d036b1cc
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon

%description
Utilities to control the kernel key management facility and to provide
a mechanism by which the kernel call back to user space to get a key
instantiated.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}
%description	devel
It contains the libraries and header files to create applications

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} LIBDIR=/%{_lib} USRLIBDIR=%{_libdir}
find %{buildroot} -name '*.a'  -delete

%clean
rm -rf %{buildroot}

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README LICENCE.GPL
/sbin/*
/bin/*
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/*.pc
%{_datadir}/keyutils
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%config(noreplace) %{_sysconfdir}/request-key.conf
%dir %{_sysconfdir}/request-key.d/

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/man3/*

%changelog
*   Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 1.6.1-1
-   Automatic Version Bump
*   Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 1.5.10-1
-   Updated to version 1.5.10
*   Fri Dec 16 2016 Dheeraj Shetty <Dheerajs@vmware.com> 1.5.9-1
-   Initial build. First version
