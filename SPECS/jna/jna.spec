Summary:	Java Native Access
Name:		jna
Version:	4.1.0
Release:	0%{?dist}
License:	Apache
URL:		http://github.com/twall/jna
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      x86_64
Source0:	http://dl.bintray.com/vmware/photon_release_1.0_TP1_x86_64/%{name}-%{version}.tar.gz
%define sha1 jna=c520c1be533619d3cbc3ad448d49a8f24ee60bda
Requires: openjdk >= 1.8.0.45
BuildRequires: openjdk >= 1.8.0.45, apache-ant >= 1.9.4

%define _prefix /opt/jna-4.1.0

%description
The JNA package contains libraries for interop from Java to native libraries.

%package devel
Summary: Sources for JNA
Group: Development/Libraries
Requires: jna = %{version}-%{release}

%description devel
Sources for JNA

%prep

%setup -q
%build
ANT_HOME=/opt/apache-ant-1.9.4
export JAVA_HOME=/opt/OpenJDK-1.8.0.51-bin

$ANT_HOME/bin/ant -Dcflags_extra.native=-DNO_JAWT -Dtests.exclude-patterns="**/LibraryLoadTest.java" -Drelease=true

%install

ANT_HOME=/opt/apache-ant-1.9.4
JNA_DIST_DIR=%{buildroot}%{_prefix}

[ %{buildroot} != "/"] && rm -rf %{buildroot}/*

mkdir -p -m 700 $JNA_DIST_DIR

$ANT_HOME/bin/ant -Ddist=$JNA_DIST_DIR dist -Drelease=true

%files
%defattr(-,root,root)
%{_prefix}/*.jar
%exclude %{_prefix}/*javadoc.jar
%exclude %{_prefix}/*sources.jar

%exclude %{_prefix}/jnacontrib/*

%files devel
%defattr(-,root,root)
%{_prefix}/src-full.zip
%{_prefix}/src.zip
%{_prefix}/doc.zip
%{_prefix}/*javadoc.jar
%{_prefix}/*sources.jar

%changelog
*   Fri May 29 2015 Sriram Nambakam <snambakam@vmware.com> 4.1.0-0
-   Initial commit
