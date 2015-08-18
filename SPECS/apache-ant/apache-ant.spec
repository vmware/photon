Summary:	Apache Ant
Name:		apache-ant
Version:	1.9.4
Release:	1%{?dist}
License:	Apache
URL:		http://ant.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:       noarch
Source0:	http://apache.mirrors.lucidnetworks.net//ant/source/%{name}-%{version}-src.tar.gz
%define sha1 apache-ant=01fe8219e50765beafc69de8b7886f882dee73ec
Source1:	http://hamcrest.googlecode.com/files/hamcrest-1.3.tar.gz
%define sha1 hamcrest=f0ab4d66186b894a06d89d103c5225cf53697db3
Source2:    http://dl.bintray.com/vmware/photon_sources/1.0/maven-ant-tasks-2.1.3.tar.gz
%define sha1 maven-ant-tasks=f38c0cc7b38007b09638366dbaa4ee902d9c255b
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
tar xf %{SOURCE2}
%build
ANT_DIST_DIR=/opt/apache-ant-1.9.4

cp -v ./hamcrest-1.3/hamcrest-core-1.3.jar ./lib/optional

mkdir -p -m 700 $ANT_DIST_DIR

export JAVA_HOME=/opt/OpenJDK-1.8.0.51-bin

./bootstrap.sh && ./build.sh -Ddist.dir=$ANT_DIST_DIR

%install

[ %{buildroot} != "/"] && rm -rf %{buildroot}/*

mkdir -p -m 700 %{buildroot}/opt

cp -r /opt/apache-ant-1.9.4 %{buildroot}/opt

cp %{_builddir}/%{name}-%{version}/maven-ant-tasks-2.1.3/maven-ant-tasks-2.1.3.jar %{buildroot}/%{_libdir}/ 

MAVEN_ANT_TASKS_DIR=%{buildroot}/opt/%{name}-%{version}/maven-ant-tasks

mkdir -p -m 700 $MAVEN_ANT_TASKS_DIR
cp %{_builddir}/%{name}-%{version}/maven-ant-tasks-2.1.3/LICENSE $MAVEN_ANT_TASKS_DIR/
cp %{_builddir}/%{name}-%{version}/maven-ant-tasks-2.1.3/NOTICE $MAVEN_ANT_TASKS_DIR/
cp %{_builddir}/%{name}-%{version}/maven-ant-tasks-2.1.3/README.txt $MAVEN_ANT_TASKS_DIR/
chown -R root:root $MAVEN_ANT_TASKS_DIR
chmod 644 $MAVEN_ANT_TASKS_DIR/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%{_prefix}/maven-ant-tasks/*

%changelog
*   Wed Aug 12 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
-   Added maven ant tasks
*	Fri May 22 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
-	Initial build.	First version
