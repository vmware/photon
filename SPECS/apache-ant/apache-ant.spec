Summary:        Apache Ant
Name:           apache-ant
Version:        1.10.12
Release:        3%{?dist}
License:        Apache
URL:            http://ant.apache.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
BuildArch:      noarch
Source0:        https://downloads.apache.org/ant/source/%{name}-%{version}-src.tar.gz
%define sha512  %{name}=1cfd31f9b19475bd94bcf59722cfc7aade58a5bb2a4f0cd6f3b90682ac6ef4cda3596269b4a91e09f2afd1be9123d4ef80db9f3c481dc34d8685b6e020a8ba11
Requires:       openjre8
BuildRequires:  openjre8
BuildRequires:  openjdk8

Patch0: 0001-Maven-Ant-tasks-has-been-EOLed-https-maven.apache.or.patch
Patch1: 0001-optional-Add-maven.resolver-ant-task-jar.patch

%define ant_prefix /var/opt/%{name}
%define ant_bindir %{ant_prefix}/bin
%define ant_libdir %{ant_prefix}/lib

%description
The Ant package contains binaries for a build system

%package -n ant-scripts
Summary:        Additional scripts for ant
Requires:       %{name} = %{version}-%{release}
Requires:       python2
%description -n ant-scripts
Apache Ant is a Java-based build tool.

This package contains additional perl and python scripts for Apache
Ant.

%prep
%autosetup -p1

%clean
rm -rf %{buildroot}

%build
ANT_DIST_DIR=%{buildroot}%{ant_prefix}
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
mkdir -p -m 700 $ANT_DIST_DIR
./bootstrap.sh && ./build.sh -Ddist.dir=$ANT_DIST_DIR
# Required to build maven-resolver-ant-task.jar
./build.sh -k -f fetch.xml -Ddest=optional

%install
mkdir -p %{buildroot}%{_datadir}/java/ant %{buildroot}%{_bindir}

cp lib/optional/maven-resolver-ant-tasks*.jar %{buildroot}/%{ant_libdir}/
for jar in %{buildroot}/%{ant_libdir}/*.jar
do
    jarname=$(basename $jar .jar)
    ln -sfv %{ant_libdir}/${jarname}.jar %{buildroot}%{_datadir}/java/ant/${jarname}.jar
done
rm -rf %{buildroot}%{ant_bindir}/*.bat
rm -rf %{buildroot}%{ant_bindir}/*.cmd

for b in %{buildroot}%{ant_bindir}/*
do
    binaryname=$(basename $b)
    ln -sfv %{ant_bindir}/${binaryname} %{buildroot}%{_bindir}/${binaryname}
done

%check
# Disable following tests which are currently failing in chrooted environment -
#   - org.apache.tools.ant.types.selectors.OwnedBySelectorTest
#   - org.apache.tools.ant.types.selectors.PosixGroupSelectorTest
#   - org.apache.tools.mail.MailMessageTest
#   - org.apache.tools.ant.AntClassLoaderTest
#   - org.apache.tools.ant.taskdefs.optional.XsltTest
if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
  rm -f src/tests/junit/org/apache/tools/ant/types/selectors/OwnedBySelectorTest.java \
        src/tests/junit/org/apache/tools/ant/types/selectors/PosixGroupSelectorTest.java \
        src/tests/junit/org/apache/tools/mail/MailMessageTest.java \
        src/tests/junit/org/apache/tools/ant/AntClassLoaderTest.java \
        src/tests/junit/org/apache/tools/ant/taskdefs/optional/XsltTest.java
fi
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
bootstrap/bin/ant -v run-tests

%files
%defattr(-,root,root)
%dir %{ant_bindir}
%dir %{ant_libdir}
%dir %{_datadir}/java/ant
%{_bindir}/ant
%{_bindir}/antRun
%{ant_bindir}/ant
%{ant_bindir}/antRun
%{ant_libdir}/*
%{_datadir}/java/ant/*.jar

%files -n ant-scripts
%defattr(-,root,root)
%{_bindir}/antRun.pl
%{_bindir}/complete-ant-cmd.pl
%{_bindir}/runant.py
%{_bindir}/runant.pl
%{ant_bindir}/antRun.pl
%{ant_bindir}/complete-ant-cmd.pl
%{ant_bindir}/runant.py
%{ant_bindir}/runant.pl

%changelog
* Tue Mar 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.10.12-3
- Bump version as a part of openjdk8 upgrade
*   Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.10.12-2
-   Bump version as a part of openjdk8 upgrade
*   Mon Nov 28 2022 Ankit Jain <ankitja@vmware.com> 1.10.12-1
-   Updated to 1.10.12
-   Replaced obsolete maven-ant-task with maven-resolver-ant-task
*   Tue Jul 20 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.10.8-3
-   Fix CVE-2021-36373, CVE-2021-36374
*   Fri Oct 16 2020 Dweep Advani <dadvani@vmware.com> 1.10.8-2
-   Patched for CVE-2020-11979
*   Wed May 27 2020 Ankit Jain <ankitja@vmware.com> 1.10.8-1
-   Updated to 1.10.8 to fix CVE-2020-1945
*   Fri Apr 24 2020 Ankit Jain <ankitja@vmware.com> 1.10.5-5
-   Changed openjdk install directory name
*   Wed Sep 11 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.10.5-4
-   Fix make check
*   Tue Dec 04 2018 Dweep Advani <dadvani@vmware.com> 1.10.5-3
-   Adding MakeCheck tests
*   Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 1.10.5-2
-   Removed dependency on JAVA8_VERSION macro
*   Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 1.10.5-1
-   Updated Apache Ant to 1.10.5
*   Wed Jun 28 2017 Kumar Kaushik <kaushikk@vmware.com> 1.10.1-5
-   Base package does not require python2.
*   Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 1.10.1-4
-   Removed dependency on ANT_HOME
-   Moved perl and python scripts to ant-scripts package
*   Mon Jun 05 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10.1-3
-   Fixed the profile.d/apache-ant.sh script to include ant in $PATH
*   Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.10.1-2
-   Renamed openjdk to openjdk8
*   Mon Apr 17 2017 Chang Lee <changlee@vmware.com> 1.10.1-1
-   Updated Apache Ant to 1.10.1
*   Fri Mar 31 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-6
-   use java rpm macros to determine versions
*   Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-5
-   Updated JAVA_HOME path to point to latest JDK.
*   Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-4
-   Updated JAVA_HOME path to point to latest JDK.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.9.6-3
-   GA - Bump release of all rpms
*   Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 1.9.6-2
-   Updated JAVA_HOME path to point to latest JDK.
*   Mon Feb 29 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.6-1
-   Updated to version 1.9.6
*   Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.9.4-4
-   Updated JAVA_HOME path to point to latest JDK.
*   Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 1.9.4-3
-   Changed path to /var/opt.
*   Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.9.4-2
-   Updated dependencies after repackaging openjdk.
*   Wed Aug 12 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
-   Added maven ant tasks
*   Fri May 22 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
-   Initial build. First version
