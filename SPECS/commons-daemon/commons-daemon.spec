Summary:        Apache Commons Daemon
Name:           commons-daemon
Version:        1.3.1
Release:        1%{?dist}
License:        Apache
URL:            https://commons.apache.org/proper/commons-daemon/download_daemon.cgi
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://mirrors.ocf.berkeley.edu/apache//commons/daemon/source/%{name}-%{version}-src.tar.gz
%define sha512  commons-daemon-%{version}-src=b810ac152f8296d980a4fb3786eff9d147b234dc2377df5fe1bded0824c694c9e82a7ef50b0a63c3e6432dfc4684a3aa2ce8d583aacb740bd4664c3dfb8b8f16
Source1:        https://mirrors.ocf.berkeley.edu/apache//commons/daemon/binaries/%{name}-%{version}-bin.tar.gz
%define sha512  commons-daemon-%{version}-bin=101fa25c723694ed7b1475a178aec40b5c94c6e8bdcfb17411841606148db25dc46825539a5afca02413fefa2566002d69310203f132edfb4e49f3018f158504
BuildRequires:  openjre8
BuildRequires:  openjdk8
BuildRequires:  apache-ant
Requires:       openjre8

%description
The Daemon Component contains a set of Java and native code,
including a set of Java interfaces applications must implement
and Unix native code to control a Java daemon from a Unix operating system.

%prep
%autosetup -n %{name}-%{version}-src
mkdir dist
cd dist
tar -xf %{SOURCE1} --no-same-owner

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-*`

%ifarch x86_64
export CFLAGS=-m64
export LDFLAGS=-m64
%endif

%ifarch aarch64
sed -i 's/supported_os="aarch64"/supported_os="linux"/' src/native/unix/configure
%endif

CURDIR=`pwd`
cd src/native/unix
%configure && make
cd $CURDIR

%install
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-*`
DIST_DIR=%{buildroot}%{_datadir}/java
mkdir -p -m 755 $DIST_DIR
mkdir -p -m 755 %{buildroot}%{_bindir}
cp %{_builddir}/%{name}-%{version}-src/src/native/unix/jsvc %{buildroot}%{_bindir}
cp %{_builddir}/%{name}-%{version}-src/dist/%{name}-%{version}/%{name}-%{version}.jar $DIST_DIR/%{name}.jar
chmod -R 755 $DIST_DIR

%files
%defattr(-,root,root)
%{_bindir}/jsvc
%{_datadir}/java/*.jar

%changelog
*   Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.3.1-1
-   Automatic Version Bump
*   Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 1.2.4-1
-   Automatic Version Bump
*   Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.3-1
-   Automatic Version Bump
*   Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.2-1
-   Automatic Version Bump
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
-   Initial commit.
