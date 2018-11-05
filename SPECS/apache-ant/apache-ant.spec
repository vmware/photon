Summary:	Apache Ant
Name:		apache-ant
Version:	1.10.5
Release:	2%{?dist}
License:	Apache
URL:		http://ant.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      noarch
Source0:	http://apache.mirrors.lucidnetworks.net//ant/source/%{name}-%{version}-src.tar.gz
%define sha1 apache-ant=ce14b7f699dcaa5b91e1f1fc642b111e42c5993d
Source1:	http://hamcrest.googlecode.com/files/hamcrest-1.3.tar.gz
%define sha1 hamcrest=f0ab4d66186b894a06d89d103c5225cf53697db3
Source2:    http://dl.bintray.com/vmware/photon_sources/1.0/maven-ant-tasks-2.1.3.tar.gz
%define sha1 maven-ant-tasks=f38c0cc7b38007b09638366dbaa4ee902d9c255b
Requires:      openjre8
BuildRequires: openjre8
BuildRequires: openjdk8
%define _prefix /var/opt/%{name}
%define _bindir %{_prefix}/bin
%define _libdir %{_prefix}/lib

%description
The Ant package contains binaries for a build system

%package -n ant-scripts
Summary:        Additional scripts for ant
Requires:       %{name} = %{version}
Requires:       python2
%description -n ant-scripts
Apache Ant is a Java-based build tool.

This package contains additional perl and python scripts for Apache
Ant.

%prep

%setup -q
tar xf %{SOURCE1} --no-same-owner
tar xf %{SOURCE2} --no-same-owner

%clean
rm -rf %{buildroot}

%build
ANT_DIST_DIR=%{buildroot}%{_prefix}
cp -v ./hamcrest-1.3/hamcrest-core-1.3.jar ./lib/optional
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-*`
mkdir -p -m 700 $ANT_DIST_DIR
./bootstrap.sh && ./build.sh -Ddist.dir=$ANT_DIST_DIR

%install
cp %{_builddir}/%{name}-%{version}/maven-ant-tasks-2.1.3/maven-ant-tasks-2.1.3.jar %{buildroot}/%{_libdir}/
mkdir -p %{buildroot}%{_datadir}/java/ant

for jar in %{buildroot}/%{_libdir}/*.jar
do
    jarname=$(basename $jar .jar)
    ln -sfv %{_libdir}/${jarname}.jar %{buildroot}%{_datadir}/java/ant/${jarname}.jar
done
rm -rf %{buildroot}%{_bindir}/*.bat
rm -rf %{buildroot}%{_bindir}/*.cmd

mkdir -p %{buildroot}/bin
for b in %{buildroot}%{_bindir}/*
do
    binaryname=$(basename $b)
    ln -sfv %{_bindir}/${binaryname} %{buildroot}/bin/${binaryname}
done

MAVEN_ANT_TASKS_DIR=%{buildroot}%{_prefix}/maven-ant-tasks

mkdir -p -m 700 $MAVEN_ANT_TASKS_DIR
cp %{_builddir}/%{name}-%{version}/maven-ant-tasks-2.1.3/LICENSE $MAVEN_ANT_TASKS_DIR/
cp %{_builddir}/%{name}-%{version}/maven-ant-tasks-2.1.3/NOTICE $MAVEN_ANT_TASKS_DIR/
cp %{_builddir}/%{name}-%{version}/maven-ant-tasks-2.1.3/README.txt $MAVEN_ANT_TASKS_DIR/
chown -R root:root $MAVEN_ANT_TASKS_DIR
chmod 644 $MAVEN_ANT_TASKS_DIR/*

%files
%defattr(-,root,root)
%dir %{_bindir}
%dir %{_libdir}
%dir %{_datadir}/java/ant
%dir %{_prefix}/maven-ant-tasks
/bin/ant
/bin/antRun
%{_bindir}/ant
%{_bindir}/antRun
%{_libdir}/*
%{_datadir}/java/ant/*.jar
%{_prefix}/maven-ant-tasks/LICENSE
%{_prefix}/maven-ant-tasks/README.txt
%{_prefix}/maven-ant-tasks/NOTICE

%files -n ant-scripts
%defattr(-,root,root)
/bin/antRun.pl
/bin/complete-ant-cmd.pl
/bin/runant.py
/bin/runant.pl
%{_bindir}/antRun.pl
%{_bindir}/complete-ant-cmd.pl
%{_bindir}/runant.py
%{_bindir}/runant.pl

%changelog
*   Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 1.10.5-2
-   Removed dependency on JAVA8_VERSION macro
*   Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 1.10.5-1
-   Updated Apache Ant to 1.10.5
*   Wed Jun 28 2017 Kumar Kaushik <kaushikk@vmware.com> 1.10.1-5
-   Base package does not require python2.
*   Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 1.10.1-4
-   Removed dependency on ANT_HOME
-   Moved perl and python scripts to ant-scripts package
*   Mon Jun 05 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10.1-3
-   Fixed the profile.d/apache-ant.sh script to include ant in $PATH
*   Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10.1-2
-   Renamed openjdk to openjdk8
*   Mon Apr 17 2017 Chang Lee <changlee@vmware.com> 1.10.1-1
-   Updated Apache Ant to 1.10.1
*   Fri Mar 31 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-6
-   use java rpm macros to determine versions
*   Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-5
-   Updated JAVA_HOME path to point to latest JDK.
*   Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-4
-   Updated JAVA_HOME path to point to latest JDK.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-3
-   GA - Bump release of all rpms
*   Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 1.9.6-2
-   Updated JAVA_HOME path to point to latest JDK.
*   Mon Feb 29 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.6-1
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
