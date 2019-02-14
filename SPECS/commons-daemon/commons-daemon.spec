Summary:	Apache Commons Daemon
Name:		commons-daemon
Version:	1.1.0
Release:	2%{?dist}
License:	Apache
URL:		http://commons.apache.org/proper/commons-daemon
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://apache.mesi.com.ar//commons/daemon/source/commons-daemon-1.1.0-src.tar.gz
%define sha1 commons-daemon=5a64221b8020d32c02bf44a115f8a95016d3c76e
BuildRequires: openjre8
BuildRequires: openjdk8
BuildRequires: apache-ant
Requires: openjre8

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

%ifarch x86_64
export CFLAGS=-m64
export LDFLAGS=-m64
%endif

%ifarch aarch64
sed -i 's/supported_os="aarch64"/supported_os="linux"/' src/native/unix/configure
%endif

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
%{_bindir}/jsvc
%{_datadir}/java/*.jar

%changelog
*   Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-2
-   Removed dependency on JAVA8_VERSION macro
*   Tue Dec 26 2017 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-1
-   Version update to support aarch64
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.0.15-12
-   Remove BuildArch
*   Tue Jun 20 2017 Divya Thaluru <dthaluru@vmware.com> 1.0.15-11
-   Packaged jar files to /usr/share/java
-   Removed version information from jar files
-   Removed dependency on ANT_HOME
*   Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0.15-10
-   Renamed openjdk to openjdk8
*   Fri Mar 31 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.15-9
-   use java rpm macros to determine versions
*   Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.15-8
-   Updated JAVA_HOME path to point to latest JDK.
*   Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.15-7
-   Updated JAVA_HOME path to point to latest JDK.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.15-6
-   GA - Bump release of all rpms
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
