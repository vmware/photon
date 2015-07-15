Summary:	Jax WS Reference Implementation
Name:		jaxws-ri
Version:	2.2.5
Release:	1%{?dist}
License:	CDDL-1.0, GPLv2
URL:		http://jax-ws.java.net/2.2.5
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      noarch
Source0:	http://jax-ws.java.net/2.2.5/%{name}-%{version}.tar.gz
%define sha1 jaxws-ri=b48b4592bd75991838d1ec003158f6b4ae05ebff
Requires: openjdk >= 1.8.0.45

%define _prefix /opt/%{name}-%{version}
%define _bindir %{_prefix}/bin
%define _libdir %{_prefix}/lib

%description
The JAX WS is a web services framework.

%prep

%setup -q -n %{name}
%build

%install

install -vdm755 %{buildroot}/%{_prefix}
mv -v %{_builddir}/%{name}/* %{buildroot}/%{_prefix}/
rm -rf %{buildroot}/%{_prefix}/samples
rm -rf %{buildroot}/%{_prefix}/docs
rm -f %{buildroot}/%{_prefix}/README
rm -f %{buildroot}/%{_prefix}/build.xml

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_prefix}/LICENSE.txt
%{_prefix}/CDDL+GPLv2.txt
%{_prefix}/ThirdPartyLicense.txt
%{_prefix}/distributionREADME_WMforJava2.0.txt
%{_bindir}/*
%{_libdir}/*.jar

%changelog
*	Thu Jul 9 2015 Sriram Nambakam <snambakam@vmware.com> 2.2.5
-	Initial build.	First version
