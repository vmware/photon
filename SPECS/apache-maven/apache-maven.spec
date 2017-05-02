Summary:	Apache Maven
Name:		apache-maven
Version:	3.5.0
Release:	1%{?dist}
License:	Apache
URL:		http://maven.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      x86_64
Source0:	http://apache.mirrors.lucidnetworks.net//maven/source/%{name}-%{version}-src.tar.gz
%define sha1 apache-maven=1730812af1cdd77493e269b371ef8ac536230c15

%define java_macros_version 1.8.0.121-1%{?dist}
Requires: openjre >= %{java_macros_version}
BuildRequires: openjre >= %{java_macros_version}
BuildRequires: openjdk >= %{java_macros_version}
BuildRequires: apache-ant >= 1.9.6
BuildRequires: wget >= 1.15

%define _prefix /var/opt/apache-maven-%{version}
%define _bindir %{_prefix}/bin
%define _libdir %{_prefix}/lib

%description
The Maven package contains binaries for a build system

%prep

%setup -q
#find . -name build.xml | xargs sed -i 's/timeout="600000"/timeout="1200000"/g'

%build
MAVEN_DIST_DIR=%{_prefix}

export JAVA_HOME=%{_java_home}
export ANT_HOME=%{_ant_home}
export PATH=$PATH:$ANT_HOME/bin
source /etc/profile.d/apache-maven.sh

sed -i 's/www.opensource/opensource/g' DEPENDENCIES

mvn -DdistributionTargetDir=$MAVEN_DIST_DIR clean package

%install
MAVEN_DIST_DIR=%{_prefix}

[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
mkdir -p -m 700 %{buildroot}/var/opt

cp -r "$MAVEN_DIST_DIR"  %{buildroot}/var/opt

# install exports file.
install -d -m 755 %{buildroot}/etc/profile.d/
echo 'export MAVEN_HOME=/var/opt/%{name}-%{version}' > %{buildroot}/etc/profile.d/%{name}.sh
echo 'export PATH=$MAVEN_HOME/bin:$PATH' >> %{buildroot}/etc/profile.d/%{name}.sh
echo 'export MAVEN_OPTS=-Xms256m' >> %{buildroot}/etc/profile.d/%{name}.sh

%files
%defattr(-,root,root)
%{_libdir}
%{_bindir}
%{_sysconfdir}/profile.d/%{name}.sh
%{_prefix}/LICENSE
%{_prefix}/NOTICE
%{_prefix}/README.txt
%{_prefix}/boot/plexus-classworlds-2.5.2.jar
%{_prefix}/conf/logging/simplelogger.properties
%{_prefix}/conf/settings.xml
%{_prefix}/conf/toolchains.xml
%exclude %{_libdir}/jansi-native

%changelog
*   Mon Apr 24 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.5.0-1
-   Updated apache-maven to version 3.5.0
*   Fri Mar 31 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.9-8
-   use java rpm macros to determine versions
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
