#need to deactivate debuginfo till we bring in x11 deps
%define debug_package %{nil}
%define _prefix %{_var}/opt/%{name}-%{version}

Summary:        Java Native Access
Name:           jna
Version:        5.12.1
Release:        5%{?dist}
URL:            https://github.com/java-native-access/jna
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/java-native-access/jna/archive/%{version}/%{name}-%{version}.tar.gz
%define sha512 %{name}-%{version}=6cabccc27792ac7779932c38b163d7d77465ebca3eff3eb7f8104fe739be1934b7b69d766dcf178bb98bb782ddbb68e89f390d6d0de1dc41ed095b5a24b33840

Source1: license.txt
%include %{SOURCE1}

Patch0: jna_remove_clover_jar.patch

BuildRequires:  openjdk11
BuildRequires:  apache-ant

Requires: (openjdk11-jre or openjdk17-jre)

%description
The JNA package contains libraries for interop from Java to native libraries.

%package        devel
Summary:        Sources for JNA
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
Sources for JNA

%prep
%autosetup -p1

%build
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK-*)

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
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK-*)
export JNA_DIST_DIR=%{buildroot}%{_prefix}

mkdir -p -m 700 $JNA_DIST_DIR

ant -Ddist=$JNA_DIST_DIR dist -Drelease=true

%check
#ignore a unicode name test which fails in chroot checks
sed -i 's/testLoadLibraryWithUnicodeName/ignore_testLoadLibraryWithUnicodeName/' \
        test/com/sun/jna/LibraryLoadTest.java
ant

%clean
rm -rf %{buildroot}

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
%{_prefix}/*.aar

%changelog
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 5.12.1-5
- Release bump for SRP compliance
* Sat Aug 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.12.1-4
- Require jdk11 or jdk17
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 5.12.1-3
- Bump version as a part of openjdk11 upgrade
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 5.12.1-2
- Use openjdk11
* Mon May 30 2022 Gerrit Photon <photon-checkins@vmware.com> 5.12.1-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 5.8.0-1
- Automatic Version Bump
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 5.6.0-2
- GCC-10 support.
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 5.6.0-1
- Automatic Version Bump
* Thu Apr 02 2020 Alexey Makhalov <amakhalov@vmware.com> 4.5.2-4
- Fix compilation issue with gcc-8.4.0
* Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 4.5.2-3
- Removed dependency on JAVA8_VERSION macro
* Thu Oct 25 2018 Ankit Jain <ankitja@vmware.com> 4.5.2-2
- Removed clover.jar from jna-devel source-full.zip file
* Mon Sep 10 2018 Ankit Jain <ankitja@vmware.com> 4.5.2-1
- Updated to version 4.5.2
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.0-9
- Remove BuildArch
* Thu Sep 14 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.4.0-8
- Makecheck for jna
* Tue Sep 05 2017 Alexey Makhalov <amakhalov@vmware.com> 4.4.0-7
- Rerun the build on failure
* Thu Aug 17 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.0-6
- Removed clover.jar from jna-devel source-full.zip file
* Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 4.4.0-5
- Removed dependency on ANT_HOME
* Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.4.0-4
- Renamed openjdk to openjdk8
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.0-3
- deactivate debuginfo temporarily - wait for x11 deps
* Tue Apr 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.4.0-2
- use java rpm macros to determine versions
* Mon Apr 03 2017 Divya Thaluru <dthaluru@vmware.com> 4.4.0-1
- Updated package to version 4.4.0
* Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.1-6
- Updated JAVA_HOME path to point to latest JDK.
* Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.1-5
- Updated JAVA_HOME path to point to latest JDK.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.2.1-4
- GA - Bump release of all rpms
* Fri May 20 2016 Divya Thaluru<dthaluru@vmware.com> 4.2.1-3
- Updated JAVA_HOME path to point to latest JDK.
* Thu Mar 03 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.2.1-2
- Updated the apache-ant version to 1.9.6
* Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 4.2.1-1
- Updating version
* Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 4.1.0-3
- Changing path to /var/optttt.
* Fri Sep 18 2015 Divya Thaluru <dthaluru@vmware.com> 4.1.0-2
- Disabling tests
* Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 4.1.0-1
- Updated dependencies after repackaging openjdk.
* Fri May 29 2015 Sriram Nambakam <snambakam@vmware.com> 4.1.0-0
- Initial commit
