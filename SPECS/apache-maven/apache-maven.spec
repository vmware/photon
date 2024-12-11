%define network_required 1
%define debug_package %{nil}

Summary:    Apache Maven
Name:       apache-maven
Version:    3.9.0
Release:    4%{?dist}
URL:        http://maven.apache.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/apache/maven/archive/refs/tags/maven-%{version}.tar.gz
%define sha512 maven=488a47b9f04889b12c2c62ea1ffec3aa071dbdd6def384b77dce259249ca49e92d7cc211a0711ff69f3b54ac7c5171bff22809089807cdaa96fc9d337fbd150c

Source1: license.txt
%include %{SOURCE1}

BuildRequires: openjdk11
BuildRequires: apache-ant
BuildRequires: wget

Requires: (openjdk11 or openjdk17)
Requires: /usr/bin/which

%define ExtraBuildRequires apache-maven

%define maven_prefix %{_var}/opt/%{name}
%define maven_bindir %{maven_prefix}/bin
%define maven_libdir %{maven_prefix}/lib

%description
The Maven package contains binaries for a build system

%prep
%autosetup -p1 -n maven-maven-%{version}

%build

%install
MAVEN_DIST_DIR=%{buildroot}%{maven_prefix}
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK-*)
mvn -DdistributionTargetDir=$MAVEN_DIST_DIR clean package

mkdir -p %{buildroot}%{_datadir}/java/maven \
         %{buildroot}%{_bindir}

for jar in %{buildroot}%{maven_libdir}/*.jar; do
  jarname=$(basename $jar .jar)
  ln -sfv %{maven_libdir}/${jarname}.jar %{buildroot}%{_datadir}/java/maven/${jarname}.jar
done

for b in %{buildroot}%{maven_bindir}/*; do
  binaryname=$(basename $b)
  ln -sfv %{maven_bindir}/${binaryname} %{buildroot}%{_bindir}/${binaryname}
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{maven_libdir}
%dir %{maven_bindir}
%dir %{maven_prefix}/conf
%dir %{maven_prefix}/boot
%dir %{_datadir}/java/maven
%{maven_libdir}/*
%{maven_bindir}/*
%{_bindir}/*
%{_datadir}/java/maven/*.jar
%{maven_prefix}/boot/plexus-classworlds-2.6.0.jar
%{maven_prefix}/boot/plexus-classworlds.license
%{maven_prefix}/conf/logging/simplelogger.properties
%{maven_prefix}/conf/settings.xml
%{maven_prefix}/conf/toolchains.xml
%{maven_prefix}/LICENSE
%{maven_prefix}/NOTICE
%{maven_prefix}/README.txt
%exclude %{maven_libdir}/jansi-native

%changelog
* Wed Dec 11 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 3.9.0-4
- Release bump for SRP compliance
* Sat Aug 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.9.0-3
- Require jdk11 or jdk17
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.9.0-2
- Bump version as a part of openjdk11 upgrade
* Fri Mar 03 2023 Srish Srinivasan <ssrish@vmware.com> 3.9.0-1
- Upgrade to v3.9.0
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 3.8.6-2
- Use openjdk11
* Sat Sep 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.8.6-1
- Upgrade to v3.8.6
* Wed Feb 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.6.3-3
- Fix binary path
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
