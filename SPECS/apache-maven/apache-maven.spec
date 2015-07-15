Summary:	Apache Maven
Name:		apache-maven
Version:	3.3.3
Release:	0
License:	Apache
URL:		http://maven.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:       noarch
Source0:	http://apache.mirrors.lucidnetworks.net//maven/source/%{name}-%{version}-src.tar.gz
%define sha1 apache-maven=70301d0669bc86cd81b25a05b1daab3c6ca23595
Requires: openjdk >= 1.8.0.45
BuildRequires: openjdk >= 1.8.0.45, apache-ant >= 1.9.4, wget >= 1.15

%define _prefix /opt/apache-maven-3.3.3
%define _bindir %{_prefix}/bin
%define _libdir %{_prefix}/lib

%description
The Maven package contains binaries for a build system

%prep

%setup -q
echo "nameserver 127.0.1.1" > /etc/resolv.conf
echo "search localdomain" >> /etc/resolv.conf
%build
MAVEN_DIST_DIR=/opt/apache-maven-3.3.3

export JAVA_HOME=/opt/OpenJDK-1.8.0.45-bin
export ANT_HOME=/opt/apache-ant-1.9.4
export PATH=$PATH:$ANT_HOME/bin

ant -Dmaven.home=$MAVEN_DIST_DIR

%install

[ %{buildroot} != "/"] && rm -rf %{buildroot}/*

mkdir -p -m 700 %{buildroot}/opt

cp -r /opt/apache-maven-3.3.3 %{buildroot}/opt

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%{_prefix}/LICENSE
%{_prefix}/NOTICE
%{_prefix}/README.txt
%{_prefix}/boot/plexus-classworlds-2.5.2.jar
%{_prefix}/conf/logging/simplelogger.properties
%{_prefix}/conf/settings.xml
%{_prefix}/conf/toolchains.xml

%changelog
*	Fri May 22 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
-	Initial build.	First version
