Summary:	Apache Ant
Name:		apache-ant
Version:	1.9.6
Release:	7%{?dist}
License:	Apache
URL:		http://ant.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:       noarch
Source0:	http://apache.mirrors.lucidnetworks.net//ant/source/%{name}-%{version}-src.tar.gz
%define sha1 apache-ant=de7c2287bca23fc32007b28e56c28f330cf7be26
Source1:	http://hamcrest.googlecode.com/files/hamcrest-1.3.tar.gz
%define sha1 hamcrest=f0ab4d66186b894a06d89d103c5225cf53697db3
Source2:    http://dl.bintray.com/vmware/photon_sources/1.0/maven-ant-tasks-2.1.3.tar.gz
%define sha1 maven-ant-tasks=f38c0cc7b38007b09638366dbaa4ee902d9c255b
Requires: openjre >= %{JAVA_VERSION}, python2
BuildRequires: openjre >= %{JAVA_VERSION}
BuildRequires: openjdk >= %{JAVA_VERSION}
%define _prefix /var/opt/apache-ant-%{version}
%define _bindir %{_prefix}/bin
%define _libdir %{_prefix}/lib

%description
The Ant package contains binaries for a build system

%prep

%setup -q
tar xf %{SOURCE1}
tar xf %{SOURCE2}
%build
ANT_DIST_DIR=/var/opt/apache-ant-%{version}

cp -v ./hamcrest-1.3/hamcrest-core-1.3.jar ./lib/optional

mkdir -p -m 700 $ANT_DIST_DIR
export JAVA_HOME=usr/lib/jvm/OpenJDK-%{JAVA_VERSION}
./bootstrap.sh && ./build.sh -Ddist.dir=$ANT_DIST_DIR

%install

[ %{buildroot} != "/"] && rm -rf %{buildroot}/*

mkdir -p -m 700 %{buildroot}/var/opt

cp -r /var/opt/apache-ant-%{version} %{buildroot}/var/opt

cp %{_builddir}/%{name}-%{version}/maven-ant-tasks-2.1.3/maven-ant-tasks-2.1.3.jar %{buildroot}/%{_libdir}/ 

MAVEN_ANT_TASKS_DIR=%{buildroot}/var/opt/%{name}-%{version}/maven-ant-tasks

mkdir -p -m 700 $MAVEN_ANT_TASKS_DIR
cp %{_builddir}/%{name}-%{version}/maven-ant-tasks-2.1.3/LICENSE $MAVEN_ANT_TASKS_DIR/
cp %{_builddir}/%{name}-%{version}/maven-ant-tasks-2.1.3/NOTICE $MAVEN_ANT_TASKS_DIR/
cp %{_builddir}/%{name}-%{version}/maven-ant-tasks-2.1.3/README.txt $MAVEN_ANT_TASKS_DIR/
chown -R root:root $MAVEN_ANT_TASKS_DIR
chmod 644 $MAVEN_ANT_TASKS_DIR/*

install -d -m 755 %{buildroot}/etc/profile.d/
echo 'export ANT_HOME=/var/opt/%{name}-%{version}' > %{buildroot}/etc/profile.d/%{name}.sh

%files
%defattr(-,root,root)
%dir %{_prefix}
%{_bindir}/*
%{_libdir}/*
%{_prefix}/maven-ant-tasks/*
%{_sysconfdir}/profile.d/%{name}.sh

%changelog
*   Fri May 19 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.6-7
-   Use Java alternatives
*	Mon May 01 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.6-6
-	Update java to 1.8.0.131 & use java macros to update version
*   Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-5
-   Updated JAVA_HOME path to point to latest JDK.
*   Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-4
-   Updated JAVA_HOME path to point to latest JDK.
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-3
-	GA - Bump release of all rpms
*   Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 1.9.6-2
-   Updated JAVA_HOME path to point to latest JDK.
*   Tue Feb 29 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.6-1
-   Updated to version 1.9.6
*   Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.9.4-4
-   Updated JAVA_HOME path to point to latest JDK.
*   Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 1.9.4-3
-   Changed path to /var/opt.
*   Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.4-2
-   Updated dependencies after repackaging openjdk.
*   Wed Aug 12 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
-   Added maven ant tasks
*   Fri May 22 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
-   Initial build.	First version
