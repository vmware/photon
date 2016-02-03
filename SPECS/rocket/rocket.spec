Summary:        Rocket
Name:           rocket
Version:        0.5.1
Release:        2%{?dist}
License:        ASL 2.0
URL:            http://rocket.readthedocs.org/en/latest/
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        rocket-v0.5.1.tar.gz
%define sha1 rocket=f04027de635f9dd965cd36dd29203dc760f5840a

%description
Rocket is a CLI for running app containers, and an implementation of the App Container Spec.
%prep
%setup -q -n %{name}-v%{version}
%build
%install
install -vdm755 %{buildroot}/bin
mv -v %{_builddir}/%{name}-v%{version}/* %{buildroot}/bin/
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
*       Mon Feb 1 2016 Alexey Makhalov <amakhalov@vmware.com> 0.5.1-2
-       Version name change: v0.5.1 -> 0.5.1
*       Fri Mar 27 2015 Fabio Rapposeli <fabio@vmware.com> 0.5.1-1
-       Initial build.  First version
