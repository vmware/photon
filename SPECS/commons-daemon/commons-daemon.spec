Summary:	Apache Commons Daemon
Name:		commons-daemon
Version:	1.0.15
Release:	10%{?dist}
License:	Apache
URL:		http://commons.apache.org/proper/commons-daemon
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      x86_64
Source0:	http://apache.mesi.com.ar//commons/daemon/source/commons-daemon-1.0.15-src.tar.gz
%define sha1 commons-daemon=ca6a448d1d214f714e214b35809a2117568970e3
BuildRequires: openjre8 >= %{JAVA8_VERSION}
BuildRequires: openjdk8 >= %{JAVA8_VERSION}
BuildRequires: apache-ant >= %{ANT_VERSION}
Requires: openjre8 >= %{JAVA8_VERSION}

%define _prefix /var/opt/%{name}-%{version}
%define _bindir %{_prefix}/bin

%description
The JNA package contains libraries for interop from Java to native libraries.

%prep

%setup -q -n %{name}-%{version}-src
%build
export ANT_HOME=/var/opt/apache-ant-%{ANT_VERSION}
export JAVA_HOME=/usr/lib/jvm/OpenJDK-%{JAVA8_VERSION}
$ANT_HOME/bin/ant dist

export CFLAGS=-m64
export LDFLAGS=-m64

CURDIR=`pwd`

cd src/native/unix && ./configure && make

cd $CURDIR

%install
export JAVA_HOME=/usr/lib/jvm/OpenJDK-%{JAVA8_VERSION}
export ANT_HOME=/var/opt/apache-ant-%{ANT_VERSION}
DIST_DIR=%{buildroot}%{_prefix}

[ %{buildroot} != "/"] && rm -rf %{buildroot}/*

mkdir -p -m 755 $DIST_DIR
mkdir -p -m 755 $DIST_DIR/bin

cp %{_builddir}/%{name}-%{version}-src/src/native/unix/jsvc $DIST_DIR/bin
cp %{_builddir}/%{name}-%{version}-src/dist/%{name}-%{version}.jar $DIST_DIR

chmod -R 755 $DIST_DIR

%files
%defattr(-,root,root)
%{_bindir}/jsvc
%{_prefix}/*.jar

%changelog
*   Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0.15-10
-   Renamed openjdk to openjdk8
*   Fri Mar 31 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.15-9
-   use java rpm macros to determine versions
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
