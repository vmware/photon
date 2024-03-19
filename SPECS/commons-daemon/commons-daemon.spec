Summary:        Apache Commons Daemon
Name:           commons-daemon
Version:        1.2.3
Release:        4%{?dist}
License:        Apache
URL:            https://commons.apache.org/proper/commons-daemon/download_daemon.cgi
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://mirrors.ocf.berkeley.edu/apache//commons/daemon/source/%{name}-%{version}-src.tar.gz
%define sha512 %{name}-%{version}-src=ddce2b90bd847f584f1d2207c5ed70b1554b9aa3a579821724a4e37d4bbaaf47425b85779216b449ee58ec9fdd38f4f3930080c8971febc7fca39dd3e73ace61

Source1: https://mirrors.ocf.berkeley.edu/apache//commons/daemon/binaries/%{name}-%{version}-bin.tar.gz
%define sha512 %{name}-%{version}-bin=0d7ced8f5d6fd3e8781146ee47c37046c6ccd2f364138f89d137eea5f0255e1b2afae5faf7005164c077087cb08203fd44478d5c14c57c7df449feb324443447

BuildRequires:  openjdk8
BuildRequires:  apache-ant

Requires: (openjre8 or openjdk11-jre or openjdk17-jre)

%description
The Daemon Component contains a set of Java and native code,
including a set of Java interfaces applications must implement
and Unix native code to control a Java daemon from a Unix operating system.

%prep
%autosetup -p1 -n %{name}-%{version}-src
mkdir -p dist
cd dist
tar -xf %{SOURCE1} --no-same-owner

%build
export JAVA_HOME=$(echo /usr/lib/jvm/OpenJDK-*)

%ifarch x86_64
export CFLAGS=-m64
export LDFLAGS=-m64
%endif

%ifarch aarch64
sed -i 's/supported_os="aarch64"/supported_os="linux"/' src/native/unix/configure
%endif

pushd src/native/unix
%configure
%make_build
popd

%install
export JAVA_HOME=$(echo /usr/lib/jvm/OpenJDK-*)
DIST_DIR=%{buildroot}%{_datadir}/java

mkdir -p -m 755 $DIST_DIR \
                %{buildroot}%{_bindir}

cp %{_builddir}/%{name}-%{version}-src/src/native/unix/jsvc %{buildroot}%{_bindir}

cp %{_builddir}/%{name}-%{version}-src/dist/%{name}-%{version}/%{name}-%{version}.jar \
       $DIST_DIR/%{name}.jar

chmod -R 755 $DIST_DIR

%files
%defattr(-,root,root)
%{_bindir}/jsvc
%{_datadir}/java/*.jar

%changelog
* Tue Mar 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.2.3-4
- Bump version as a part of openjdk8 upgrade
* Fri Sep 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2.3-3
- Require jre8 or jdk11-jre or jdk17-jre
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.2.3-2
- Bump version as a part of openjdk8 upgrade
* Mon Sep 21 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.3-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.2-1
- Automatic Version Bump
* Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-2
- Removed dependency on JAVA8_VERSION macro
* Tue Dec 26 2017 Alexey Makhalov <amakhalov@vmware.com> 1.1.0-1
- Version update to support aarch64
* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.0.15-12
- Remove BuildArch
* Tue Jun 20 2017 Divya Thaluru <dthaluru@vmware.com> 1.0.15-11
- Packaged jar files to /usr/share/java
- Removed version information from jar files
- Removed dependency on ANT_HOME
* Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0.15-10
- Renamed openjdk to openjdk8
* Fri Mar 31 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.15-9
- use java rpm macros to determine versions
* Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.15-8
- Updated JAVA_HOME path to point to latest JDK.
* Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.15-7
- Updated JAVA_HOME path to point to latest JDK.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.15-6
- GA - Bump release of all rpms
* Fri May 20 2016 Divya Thaluru<dthaluru@vmware.com> 1.0.15-5
- Updated JAVA_HOME path to point to latest JDK.
* Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0.15-4
- Updated JAVA_HOME path to point to latest JDK.
* Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 1.0.15-3
- Changing path to /var/opt.
* Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0.15-2
- Updated dependencies after repackaging openjdk.
* Wed Jul 15 2015 Sriram Nambakam <snambakam@vmware.com> 1.0.15-1
- Initial commit
