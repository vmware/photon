Summary:	Jax WS Reference Implementation
Name:		jaxws-ri
Version:	2.2.10
Release:	4%{?dist}
License:	CDDL-1.0, GPLv2
URL:		http://jax-ws.java.net/%{version}
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      noarch
Source0:	http://jax-ws.java.net/%{version}/%{name}-%{version}.tar.gz
%define sha1 jaxws-ri=0f2f00cfd3783f94fa940cc8ef678d47fb748c8c
Requires: openjre8 >= 1.8.0.45

%define _prefix /opt/%{name}
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

rm -f %{buildroot}/%{_bindir}/*.bat

mkdir -p %{buildroot}%{_datadir}/java/jaxws-ri

for jar in %{buildroot}/%{_libdir}/*.jar
do
    jarname=$(basename $jar .jar)
    ln -sfv %{_libdir}/${jarname}.jar %{buildroot}%{_datadir}/java/jaxws-ri/${jarname}.jar
done

mkdir -p %{buildroot}%{_datadir}/java/jaxws-ri/plugins

for jar in %{buildroot}/%{_libdir}/plugins/*.jar
do
    jarname=$(basename $jar .jar)
    ln -sfv %{_libdir}/plugins/${jarname}.jar %{buildroot}%{_datadir}/java/jaxws-ri/plugins/${jarname}.jar
done

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%dir %{_prefix}
%dir %{_bindir}
%dir %{_libdir}
%dir %{_datadir}/java/jaxws-ri
%dir %{_datadir}/java/jaxws-ri/plugins
%{_prefix}/LICENSE.txt
%{_prefix}/CDDL+GPLv2.txt
%{_prefix}/ThirdPartyLicense.txt
%{_prefix}/distributionREADME_WMforJava2.0.txt
%{_bindir}/*
%{_libdir}/*.jar
%{_libdir}/plugins/*.jar
%{_datadir}/java/jaxws-ri/*.jar
%{_datadir}/java/jaxws-ri/plugins/*.jar

%changelog
*	Mon Jul 10 2017 Divya Thaluru <dthaluru@vmware.com> 2.2.10-4
-	Removed version dependency on installed directory
-	Enabled symlinks to /usr/share/java
*	Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.2.10-3
-	Renamed openjdk to openjdk8
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.2.10-2
-	GA - Bump release of all rpms
* 	Tue Feb 23 2016 Anish Swaminathan <anishs@vmware.com>  2.2.10-1
- 	Upgrade to 2.2.10
*	Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.2.5-2
-	Updated dependency after repackaging openjdk.
*	Thu Jul 9 2015 Sriram Nambakam <snambakam@vmware.com> 2.2.5
-	Initial build.	First version
