Summary:	Java Native Access
Name:		jna
Version:	4.2.1
Release:	5%{?dist}
License:	Apache
URL:		http://github.com/twall/jna
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      x86_64
Source0:	http://dl.bintray.com/vmware/photon_release_1.0_TP1_x86_64/%{name}-%{version}.tar.gz
%define sha1 jna=30a1132f9ca6b3222eccd380a3f4149aa7df3f59
Requires: openjre >= 1.8.0.102
BuildRequires: openjre >= 1.8.0.45, openjdk >= 1.8.0.45, apache-ant >= 1.9.6

%define _prefix /var/opt/jna-4.2.1

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
ANT_HOME=/var/opt/apache-ant-1.9.6
export JAVA_HOME=/var/opt/OpenJDK-1.8.0.102-bin

#disabling all tests
$ANT_HOME/bin/ant -Dcflags_extra.native=-DNO_JAWT -Dtests.exclude-patterns="**/*.java" -Drelease=true
#$ANT_HOME/bin/ant -Dcflags_extra.native=-DNO_JAWT -Dtests.exclude-patterns="**/LibraryLoadTest.java" -Drelease=true

%install

ANT_HOME=/var/opt/apache-ant-1.9.6
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
*   Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.1-5
-   Updated JAVA_HOME path to point to latest JDK.
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.1-4
-	GA - Bump release of all rpms
*   Fri May 20 2016 Divya Thaluru<dthaluru@vmware.com> 4.2.1-3
-   Updated JAVA_HOME path to point to latest JDK.
* 	Thu Mar 03 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.1-2
    Updated the apache-ant version to 1.9.6
*   Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 4.2.1-1
-   Updating version
*   Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 4.1.0-3
-   Changing path to /var/optttt.
*   Fri Sep 18 2015 Divya Thaluru <dthaluru@vmware.com> 4.1.0-2
-   Disabling tests
*   Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.1.0-1
-   Updated dependencies after repackaging openjdk. 
*   Fri May 29 2015 Sriram Nambakam <snambakam@vmware.com> 4.1.0-0
-   Initial commit
