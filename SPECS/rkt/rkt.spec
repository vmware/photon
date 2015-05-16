Summary:        rkt
Name:           rkt
Version:        v0.5.5
Release:        2
License:        ASL 2.0
URL:            https://coreos.com/rkt/docs/
Group:          Applications/File
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/coreos/rkt/releases/download/%{name}-%{version}.tar.gz

%description
rkt is a CLI for running app containers, and an implementation of the App Container Spec.
%prep
%autosetup
%build
%install
install -vdm755 %{buildroot}/bin
install -vm755 %{_builddir}/%{name}-%{version}/rkt %{buildroot}/bin/
install -vm644 %{_builddir}/%{name}-%{version}/stage1.aci %{buildroot}/bin/
%check
%clean
rm -rf %{buildroot}
%files
/bin/*
%changelog
*       Wed May 13 2015 Tom McPhail <tmcphail@vmware.com> 0.5.5-1
-       Updated rkt to 0.5.5 and revised spec
*       Fri Mar 27 2015 Fabio Rapposeli <fabio@vmware.com> 0.5.1-1
-       Initial build.  First version
