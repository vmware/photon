Summary:	Apache Commons Daemon
Name:		commons-daemon
Version:	1.0.15
Release:	1%{?dist}
License:	Apache
URL:		http://commons.apache.org/proper/commons-daemon
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      x86_64
Source0:	http://apache.mesi.com.ar//commons/daemon/source/commons-daemon-1.0.15-src.tar.gz
%define sha1 commons-daemon=ca6a448d1d214f714e214b35809a2117568970e3
Requires: openjdk >= 1.8.0.45
BuildRequires: openjdk >= 1.8.0.45, apache-ant >= 1.9.4

%define _prefix /opt/%{name}-%{version}
%define _bindir %{_prefix}/bin

%description
The JNA package contains libraries for interop from Java to native libraries.

%prep

%setup -q -n %{name}-%{version}-src
%build
ANT_HOME=/opt/apache-ant-1.9.4
export JAVA_HOME=/opt/OpenJDK-1.8.0.51-bin

$ANT_HOME/bin/ant dist

export CFLAGS=-m64
export LDFLAGS=-m64

CURDIR=`pwd`

cd src/native/unix && ./configure && make

cd $CURDIR

%install

ANT_HOME=/opt/apache-ant-1.9.4
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
*   Wed Jul 15 2015 Sriram Nambakam <snambakam@vmware.com> 1.0.15-1
-   Initial commit
