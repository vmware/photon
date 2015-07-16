Summary:	Apache Tomcat
Name:		apache-tomcat
Version:	7.0.63
Release:	1%{?dist}
License:	Apache
URL:		http://tomcat.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      noarch
Source0:	http://mirrors.gigenet.com/apache/tomcat/tomcat-7/v7.0.63/src/%{name}-%{version}.tar.gz
%define sha1 apache-tomcat=ddd520f6df2414f10b6b0832dcacd7889f2dbff0
Requires: openjdk >= 1.8.0.45

%define _prefix /opt/%{name}-%{version}
%define _bindir %{_prefix}/bin
%define _confdir %{_prefix}/conf
%define _libdir %{_prefix}/lib
%define _webappsdir %{_prefix}/webapps

%description
The Apache Tomcat package contains binaries for the Apache Tomcat servlet container.

%prep

%setup -q
%build

%install

install -vdm755 %{buildroot}/opt/%{name}-%{version}
mv -v %{_builddir}/%{name}-%{version}/* %{buildroot}/opt/%{name}-%{version}/
rm -rf %{buildroot}/opt/%{name}-%{version}/webapps/examples
rm -rf %{buildroot}/opt/%{name}-%{version}/webapps/work
rm -rf %{buildroot}/opt/%{name}-%{version}/webapps/temp
rm -rf %{buildroot}/opt/%{name}-%{version}/webapps/docs
rm -rf %{buildroot}/opt/%{name}-%{version}/temp
rm -f %{buildroot}/opt/%{name}-%{version}/RUNNING.txt
rm -f %{buildroot}/opt/%{name}-%{version}/RELEASE-NOTES

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_prefix}/LICENSE
%{_prefix}/NOTICE
%{_bindir}/*
%{_confdir}/*
%{_libdir}/*
%{_webappsdir}/*

%changelog
*	Wed Jul 8 2015 Sriram Nambakam <snambakam@vmware.com> 7.0.63
-	Initial build.	First version
