Summary:	Apache Maven
Name:		apache-maven
Version:	3.3.9
Release:	11%{?dist}
License:	Apache
URL:		http://maven.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:       noarch
Source0:	http://apache.mirrors.lucidnetworks.net//maven/source/%{name}-%{version}-src.tar.gz
%define sha1 apache-maven=1912316078f1f7041dd8cd2580f210d30f898162
BuildRequires: openjre
BuildRequires: openjdk
BuildRequires: apache-ant
BuildRequires: wget >= 1.15
Requires: openjre

%define _prefix /var/opt/%{name}
%define _bindir %{_prefix}/bin
%define _libdir %{_prefix}/lib

%description
The Maven package contains binaries for a build system

%prep

%setup -q
find . -name build.xml | xargs sed -i 's/timeout="600000"/timeout="1200000"/g'

%clean
rm -rf %{buildroot}

%build
MAVEN_DIST_DIR=%{buildroot}%{_prefix}
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-*`

sed -i 's/www.opensource/opensource/g' DEPENDENCIES
ant -Dmaven.home=$MAVEN_DIST_DIR

%install
mkdir -p %{buildroot}%{_datadir}/java/maven

for jar in %{buildroot}/%{_libdir}/*.jar
do
    jarname=$(basename $jar .jar)
    ln -sfv %{_libdir}/${jarname}.jar %{buildroot}%{_datadir}/java/maven/${jarname}.jar
done

mkdir -p %{buildroot}/bin
for b in %{buildroot}%{_bindir}/*
do
    binaryname=$(basename $b)
    ln -sfv %{_bindir}/${binaryname} %{buildroot}/bin/${binaryname}
done

%files
%defattr(-,root,root)
%dir %{_libdir}
%dir %{_bindir}
%dir %{_prefix}/conf
%dir %{_prefix}/boot
%dir %{_datadir}/java/maven
%{_libdir}/*
%{_bindir}/*
/bin/*
%{_prefix}/LICENSE
%{_prefix}/NOTICE
%{_prefix}/README.txt
%{_datadir}/java/maven/*.jar
%{_prefix}/boot/plexus-classworlds-2.5.2.jar
%{_prefix}/conf/logging/simplelogger.properties
%{_prefix}/conf/settings.xml
%{_prefix}/conf/toolchains.xml

%changelog
*   Fri Mar 15 2019 Ankit Jain <ankitja@vmware.com> 3.3.9-11
-   Removed JAVA_VERSION macro
*   Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 3.3.9-10
-   Removed dependency on ANT_HOME
-   Removed apache-maven profile file
-   Removed version from directory path
*   Fri May 19 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.3.9-9
-   Remove macros and use java alternatives
*   Mon May 01 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.3.9-8
-   Update java to 1.8.0.131 & use java macros to update version
*   Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.9-7
-   Updated JAVA_HOME path to point to latest JDK.
*   Thu Oct 27 2016 Alexey Makhalov <amakhalov@vmware.com> 3.3.9-6
-   Fix build issue - unable to fetch opensource.org/.../mit-license.php
*   Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.9-5
-   Updated JAVA_HOME path to point to latest JDK.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.9-4
-   GA - Bump release of all rpms
*   Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 3.3.9-3
-   Updated JAVA_HOME path to point to latest JDK.
*   Tue Mar 01 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.3.9-2
-   Updated the apache-ant version to 1.9.6
*   Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 3.3.9-2
-   Updated JAVA_HOME path to point to latest JDK.
*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 3.3.9-1
-   Updated to version 3.3.9
*   Tue Jan 5 2016 Xiaolin Li <xiaolinl@vmware.com> 3.3.3-4
-   Increase build timeout from 600000 to 1200000
*   Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 3.3.3-3
-   Change path to /var/opt.
*   Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.3.3-2
-   Updated dependencies after repackaging openjdk.
*   Thu Jul 9 2015 	Sarah Choi<sarahc@vmware.com> 3.3.3-1
-   Add a script to set environment variables for MAVEN
*   Fri May 22 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
-   Initial build.	First version
