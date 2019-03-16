# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

Summary:	Java Native Access
Name:		jna
Version:	4.2.1
Release:	11%{?dist}
License:	Apache
URL:		http://github.com/twall/jna
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      x86_64
Source0:	http://dl.bintray.com/vmware/photon_release_1.0_TP1_x86_64/%{name}-%{version}.tar.gz
Patch0:         jna-4.2.1-remove-clover-jar.patch
%define sha1 jna=30a1132f9ca6b3222eccd380a3f4149aa7df3f59
Requires: openjre
BuildRequires: openjre
BuildRequires: openjdk
BuildRequires: apache-ant

%define _prefix /var/opt/%{name}-%{version}

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
%patch0 -p1

%clean
rm -rf %{buildroot}

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-*`
# Intermittent issue happens:
#
# BUILD FAILED
# /usr/src/photon/BUILD/jna-4.4.0/build.xml:717: API for native code has changed, or javah output is inconsistent.
# Re-run this build after checking /usr/src/photon/BUILD/jna-4.4.0/build/native-linux-x86-64/jni.checksum or updating jni.version and jni.md5 in build.xml
#
# Rerun the build will pass it
ant -Dcflags_extra.native=-DNO_JAWT -Dtests.exclude-patterns="**/*.java" -Drelease=true || \
ant -Dcflags_extra.native=-DNO_JAWT -Dtests.exclude-patterns="**/*.java" -Drelease=true

%install
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-*`
export JNA_DIST_DIR=%{buildroot}%{_prefix}

mkdir -p -m 700 $JNA_DIST_DIR

ant -Ddist=$JNA_DIST_DIR dist -Drelease=true

%files
%defattr(-,root,root)
%dir %{_prefix}
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
*   Fri Mar 15 2019 Ankit Jain <ankitja@vmware.com> 4.2.1-11
-   Removed JAVA_VERSION macro
*   Thu Aug 17 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.1-10
-   Remove clover.jar from jna-devel
*   Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 4.2.1-9
-   Removed dependency on ANT_HOME
*   Mon May 01 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.1-8
-   Use java alternatives and remove macros
*   Mon May 01 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.1-7
-   Update java to 1.8.0.131 & use java macros to update version
*   Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.1-6
-   Updated JAVA_HOME path to point to latest JDK.
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
