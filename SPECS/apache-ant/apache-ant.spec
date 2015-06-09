Summary:	Apache Ant
Name:		apache-ant
Version:	1.9.4
Release:	0%{?dist}
License:	Apache
URL:		http://ant.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:       noarch
Source0:	http://apache.mirrors.lucidnetworks.net//ant/source/%{name}-%{version}-src.tar.gz
Source1:	http://hamcrest.googlecode.com/files/hamcrest-1.3.tar.gz
Requires: openjdk >= 1.8.0.45, python2
BuildRequires: openjdk >= 1.8.0.45

%define _prefix /opt/apache-ant-1.9.4
%define _bindir %{_prefix}/bin
%define _libdir %{_prefix}/lib

%description
The Ant package contains binaries for a build system

%prep

%setup -q
tar xf %{SOURCE1}
%build
ANT_DIST_DIR=/opt/apache-ant-1.9.4

cp -v ./hamcrest-1.3/hamcrest-core-1.3.jar ./lib/optional

mkdir -p -m 700 $ANT_DIST_DIR

export JAVA_HOME=/opt/OpenJDK-1.8.0.45-bin

./bootstrap.sh && ./build.sh -Ddist.dir=$ANT_DIST_DIR

%install

[ %{buildroot} != "/"] && rm -rf %{buildroot}/*

mkdir -p -m 700 %{buildroot}/opt

cp -r /opt/apache-ant-1.9.4 %{buildroot}/opt

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*

%changelog
*	Fri May 22 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
-	Initial build.	First version
