Summary:        Rocket
Name:           rocket
Version:        1.4.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            http://rocket.readthedocs.org/en/latest/
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        rkt-v1.4.0.tar.gz
%define sha1 rkt=f1efb94ea08fc9917b7da1c1913c8d45b814e8f8

%description
Rocket is a CLI for running app containers, and an implementation of the App Container Spec.
%prep
%setup -q -n rkt-v%{version}
%build
%install
install -vdm755 %{buildroot}/bin
mv -v %{_builddir}/rkt-v%{version}/* %{buildroot}/bin/
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
%changelog
*       Fri Apr 15 2016 Kumar Kaushik <kaushikk@vmware.com> 1.4.0-1
-       Updated version.
*       Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.0-1
-       Updated to version 1.0.0
*       Mon Feb 1 2016 Alexey Makhalov <amakhalov@vmware.com> 0.5.1-2
-       Version name change: v0.5.1 -> 0.5.1
*       Fri Mar 27 2015 Fabio Rapposeli <fabio@vmware.com> 0.5.1-1
-       Initial build.  First version
