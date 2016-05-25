Summary:        Rocket
Name:           rocket
Version:        1.4.0
Release:        3%{?dist}
License:        ASL 2.0
URL:            http://rocket.readthedocs.org/en/latest/
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        rkt-v1.4.0.tar.gz
BuildRequires:  systemd
%define sha1 rkt=f1efb94ea08fc9917b7da1c1913c8d45b814e8f8

%description
Rocket is a CLI for running app containers, and an implementation of the App Container Spec.
%prep
%setup -q -n rkt-v%{version}
%build
%install
install -vdm755 %{buildroot}/bin
install -vdm755 %{buildroot}/usr/lib/systemd/system
mv -v %{_builddir}/rkt-v%{version}/rkt %{buildroot}/bin/
mv -v %{_builddir}/rkt-v%{version}/*.aci %{buildroot}/bin/
mv -v %{_builddir}/rkt-v%{version}/scripts/setup-data-dir.sh %{buildroot}/bin/
mv -v %{_builddir}/rkt-v%{version}/init/systemd/rkt-* %{buildroot}/usr/lib/systemd/system/
install -vdm755 %{buildroot}/var/lib/rkt
install -vdm755 %{buildroot}/var/lib/rkt/cas
install -vdm755 %{buildroot}/var/lib/rkt/cas/db
install -vdm755 %{buildroot}/var/lib/rkt/tmp
install -vdm755 %{buildroot}/var/lib/rkt/containers

%{_fixperms} %{buildroot}/*
%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}
%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/bin/*
/usr/lib/systemd/system/*
/var/lib/rkt
/var/lib/rkt/cas
/var/lib/rkt/cas/db
/var/lib/rkt/tmp
/var/lib/rkt/containers

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com>         1.4.0-3
-	GA - Bump release of all rpms
*       Mon Apr 18 2016 Kumar Kaushik <kaushikk@vmware.com> 1.4.0-2
-       Adding missing files.
*       Fri Apr 15 2016 Kumar Kaushik <kaushikk@vmware.com> 1.4.0-1
-       Updated version.
*       Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.0-1
-       Updated to version 1.0.0
*       Mon Feb 1 2016 Alexey Makhalov <amakhalov@vmware.com> 0.5.1-2
-       Version name change: v0.5.1 -> 0.5.1
*       Fri Mar 27 2015 Fabio Rapposeli <fabio@vmware.com> 0.5.1-1
-       Initial build.  First version
