%define _prefix %{_var}/opt/%{name}

Summary:    Apache commons-httpclient
Name:       commons-httpclient
Version:    3.1
Release:    4%{?dist}
License:    Apache
URL:        http://ant.apache.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0: https://archive.apache.org/dist/httpcomponents/%{name}/source/%{name}-%{version}-src.tar.gz
%define sha512  %{name}=e73ceeba3f34a35c30b24a3c6cb8dfc2102ff21079a5ff9270935908cb2f707d366c2f31a53fbdafa99673cc2b82e05470a2bf40d96767c72b2ab037c0f55490

# Bundled below jar into tarball
# https://repo.maven.apache.org/maven2/commons-logging/commons-logging/1.0.4/commons-logging-1.0.4.jar
# https://repo.maven.apache.org/maven2/commons-codec/commons-codec/1.2/commons-codec-1.2.jar
# https://repo.maven.apache.org/maven2/junit/junit/3.8.1/junit-3.8.1.jar
Source1: %{name}-buildrequires-jars-%{version}.tar.gz
%define sha512 %{name}-buildrequires-jars=0d1e4afda7dcb3b261c97a345a67ce9ec9e5e20ddd501637b8edd4a2ba6b02e848e3dbfb2ec3457c8347d46e0ac1343313afaa8841d7308fb070b382f085ec19

Patch0:         jakarta-commons-httpclient-encoding.patch
Patch1:         06_fix_CVE-2012-5783.patch
Patch2:         CVE-2014-3577.patch
Patch3:         CVE-2015-5262.patch

BuildRequires:  wget
BuildRequires:  openjdk8
BuildRequires:  apache-ant

Requires: (openjre8 or openjdk11-jre or openjdk17-jre)

%description
The Hyper-Text Transfer Protocol (HTTP) is perhaps the most significant
protocol used on the Internet today. Web services, network-enabled
appliances and the growth of network computing continue to expand the
role of the HTTP protocol beyond user-driven web browsers, while
increasing the number of applications that require HTTP support.

%prep
%autosetup -p1

mkdir -p target/dependency
tar -xf %{SOURCE1} -C target/dependency --no-same-owner
pushd target/dependency
cp %{name}-buildrequires-jars-%{version}/*.jar .
popd

%build
export JAVA_HOME=$(echo /usr/lib/jvm/OpenJDK*)

ant -Ddist.dir="." \
    -Dbuild.sysclasspath=first \
    -Dtest.failonerror=false \
    -Dlib.dir=./target/dependency \
    -Djavac.encoding=UTF-8 \
    dist

%install
export JAVA_HOME=$(echo /usr/lib/jvm/OpenJDK*)

mkdir -p -m 700 %{buildroot}%{_prefix} \
                %{buildroot}%{_datadir}/java/%{name}

cp -r dist/commons-httpclient.jar %{buildroot}%{_prefix}/
cp -r dist/commons-httpclient.jar %{buildroot}%{_datadir}/java/%{name}/

pushd %{buildroot}%{_prefix}
ln -s commons-httpclient.jar apache-commons-httpclient.jar
popd

pushd %{buildroot}%{_datadir}/java/%{name}
ln -s commons-httpclient.jar apache-commons-httpclient.jar
popd

cp dist/{LICENSE.txt,README.txt} %{buildroot}%{_prefix}/

%check
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK*)
ant -Ddist.dir="." \
    -Dbuild.sysclasspath=first \
    -Dtest.failonerror=false \
    -Dlib.dir=./target/dependency \
    -Djavac.encoding=UTF-8 \
    test

%files
%defattr(-,root,root)
%dir %{_prefix}
%{_prefix}/LICENSE.txt
%{_prefix}/README.txt
%{_prefix}/*.jar
%dir %{_datadir}/java/%{name}
%{_datadir}/java/%{name}/*.jar

%changelog
* Tue Mar 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 3.1-4
- Bump version as a part of openjdk8 upgrade
* Fri Sep 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.1-3
- Require jre8 or jdk11-jre or jdk17-jre
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.1-2
- Bump version as a part of openjdk8 upgrade
* Thu Sep 10 2020 Ankit Jain <ankitja@vmware.com> 3.1-1
- Initial build. First version
