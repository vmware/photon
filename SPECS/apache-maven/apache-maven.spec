%define ExtraBuildRequires apache-maven

%define _prefix %{_var}/opt/%{name}
%define _bindir %{_prefix}/bin
%define _libdir %{_prefix}/lib

Summary:    Apache Maven
Name:       apache-maven
Version:    3.6.3
Release:    5%{?dist}
License:    Apache License 2.0
URL:        http://maven.apache.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: http://mirrors.wuchna.com/apachemirror/maven/maven-3/%{version}/source/%{name}-%{version}-src.tar.gz
%define sha512 %{name}=14eef64ad13c1f689f2ab0d2b2b66c9273bf336e557d81d5c22ddb001c47cf51f03bb1465d6059ce9fdc2e43180ceb0638ce914af1f53af9c2398f5d429f114c

BuildRequires: openjdk8
BuildRequires: apache-ant

Requires: (openjdk8 or openjdk11 or openjdk17)
Requires: /usr/bin/which

%description
The Maven package contains binaries for a build system

%prep
%autosetup -p1

%build

%install
MAVEN_DIST_DIR=%{buildroot}%{_prefix}
export JAVA_HOME=$(echo /usr/lib/jvm/OpenJDK-*)
sed -i 's/www.opensource/opensource/g' DEPENDENCIES
mvn -DdistributionTargetDir=$MAVEN_DIST_DIR clean package

mkdir -p %{buildroot}%{_datadir}/java/maven
for jar in %{buildroot}/%{_libdir}/*.jar; do
  jarname=$(basename $jar .jar)
  ln -sfv %{_libdir}/${jarname}.jar %{buildroot}%{_datadir}/java/maven/${jarname}.jar
done

mkdir -p %{buildroot}/bin
for b in %{buildroot}%{_bindir}/*; do
  binaryname=$(basename $b)
  ln -sfv %{_bindir}/${binaryname} %{buildroot}/bin/${binaryname}
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_libdir}
%dir %{_bindir}
%dir %{_prefix}/conf
%dir %{_prefix}/boot
%dir %{_datadir}/java/maven
%{_libdir}/*
%{_bindir}/*
/bin/*
%{_datadir}/java/maven/*.jar
%{_prefix}/boot/plexus-classworlds-2.6.0.jar
%{_prefix}/boot/plexus-classworlds.license
%{_prefix}/conf/logging/simplelogger.properties
%{_prefix}/conf/settings.xml
%{_prefix}/conf/toolchains.xml
%{_prefix}/LICENSE
%{_prefix}/NOTICE
%{_prefix}/README.txt
%exclude %{_libdir}/jansi-native

%changelog
* Tue Mar 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.6.3-5
- Bump version as a part of openjdk8 upgrade
* Fri Sep 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.6.3-4
- Require jre8 or jdk11-jre or jdk17-jre
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.6.3-3
- Bump version as a part of openjdk8 upgrade
* Tue Dec 15 2020 Shreenidhi Shedi <sshedi@vmware.com> 3.6.3-2
- Fix build with new rpm
* Tue Jun 30 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 3.6.3-1
- Update to 3.6.3
* Fri Apr 17 2020 Tapas Kundu <tkundu@vmware.com> 3.5.4-4
- Fix apache-maven build failure
* Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 3.5.4-3
- Removed dependency on JAVA8_VERSION macro
* Mon Oct 29 2018 Alexey Makhalov <amakhalov@vmware.com> 3.5.4-2
- Use ExtraBuildRequires
* Tue Sep 18 2018 Ankit Jain <ankitja@vmware.com> 3.5.4-1
- Updated apache-maven to version 3.5.4
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 3.5.0-5
- Remove BuildArch
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.5.0-4
- Requires /usr/bin/which
* Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 3.5.0-3
- Removed dependency on ANT_HOME
- Removed apache-maven profile file
- Removed version from directory path
* Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.5.0-2
- Renamed openjdk to openjdk8
* Mon Apr 24 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.5.0-1
- Updated apache-maven to version 3.5.0
* Fri Mar 31 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.9-8
- use java rpm macros to determine versions
* Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.9-7
- Updated JAVA_HOME path to point to latest JDK.
* Thu Oct 27 2016 Alexey Makhalov <amakhalov@vmware.com> 3.3.9-6
- Fix build issue - unable to fetch opensource.org/.../mit-license.php
* Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.9-5
- Updated JAVA_HOME path to point to latest JDK.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.3.9-4
- GA - Bump release of all rpms
* Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 3.3.9-3
- Updated JAVA_HOME path to point to latest JDK.
* Tue Mar 01 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.3.9-2
- Updated the apache-ant version to 1.9.6
* Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 3.3.9-2
- Updated JAVA_HOME path to point to latest JDK.
* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 3.3.9-1
- Updated to version 3.3.9
* Tue Jan 5 2016 Xiaolin Li <xiaolinl@vmware.com> 3.3.3-4
- Increase build timeout from 600000 to 1200000
* Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 3.3.3-3
- Change path to /var/opt.
* Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.3.3-2
- Updated dependencies after repackaging openjdk.
* Thu Jul 9 2015    Sarah Choi<sarahc@vmware.com> 3.3.3-1
- Add a script to set environment variables for MAVEN
* Fri May 22 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
- Initial build.    First version
