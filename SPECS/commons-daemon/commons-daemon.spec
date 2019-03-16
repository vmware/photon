Summary:	Apache Commons Daemon
Name:		commons-daemon
Version:	1.0.15
Release:	12%{?dist}
License:	Apache
URL:		http://commons.apache.org/proper/commons-daemon
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      x86_64
Source0:	http://apache.mesi.com.ar//commons/daemon/source/commons-daemon-1.0.15-src.tar.gz
%define sha1 commons-daemon=ca6a448d1d214f714e214b35809a2117568970e3
BuildRequires: openjre
BuildRequires: openjdk
BuildRequires: apache-ant
Requires: openjre

%description
The Daemon Component contains a set of Java and native code, including a set of Java interfaces applications must implement and Unix native
code to control a Java daemon from a Unix operating system.

%prep

%setup -q -n %{name}-%{version}-src

%clean
rm -rf %{buildroot}

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-*`
ant dist

export CFLAGS=-m64
export LDFLAGS=-m64

CURDIR=`pwd`

cd src/native/unix && ./configure && make

cd $CURDIR

%install
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-*`
DIST_DIR=%{buildroot}%{_datadir}/java

mkdir -p -m 755 $DIST_DIR
mkdir -p -m 755 %{buildroot}%{_bindir}

cp %{_builddir}/%{name}-%{version}-src/src/native/unix/jsvc %{buildroot}%{_bindir}
cp %{_builddir}/%{name}-%{version}-src/dist/%{name}-%{version}.jar $DIST_DIR/%{name}.jar

chmod -R 755 $DIST_DIR

%files
%defattr(-,root,root)
%dir %{_prefix}
%{_bindir}/jsvc
%{_datadir}/java/*.jar

%changelog
*   Fri Mar 15 2019 Ankit Jain <ankitja@vmware.com> 1.0.15-12
-   Removed JAVA_VERSION macro
*   Tue Jun 20 2017 Divya Thaluru <dthaluru@vmware.com> 1.0.15-11
-   Packaged jar files to /usr/share/java
-   Removed version information from jar files
-   Removed dependency on ANT_HOME
*   Fri May 19 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0.15-10
-   Use java alternatives and remove macros
*	Mon May 01 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0.15-9
-	Update java to 1.8.0.131 & use java macros to update version
*   Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.15-8
-   Updated JAVA_HOME path to point to latest JDK.
*   Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.15-7
-   Updated JAVA_HOME path to point to latest JDK.
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.15-6
-	GA - Bump release of all rpms
*   Fri May 20 2016 Divya Thaluru<dthaluru@vmware.com> 1.0.15-5
-   Updated JAVA_HOME path to point to latest JDK.
*   Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0.15-4
-   Updated JAVA_HOME path to point to latest JDK.
*   Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 1.0.15-3
-   Changing path to /var/opt.
*   Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0.15-2
-   Updated dependencies after repackaging openjdk.
*   Wed Jul 15 2015 Sriram Nambakam <snambakam@vmware.com> 1.0.15-1
-   Initial commit
