%define _prefix %{_var}/opt/%{name}

Summary:    Apache commons-httpclient
Name:       commons-httpclient
Version:    3.1
Release:    6%{?dist}
URL:        http://ant.apache.org
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon

BuildArch:      noarch

Source0: https://archive.apache.org/dist/httpcomponents/%{name}/source/%{name}-%{version}-src.tar.gz

# Bundled below jar into tarball
# https://repo.maven.apache.org/maven2/commons-logging/commons-logging/1.0.4/commons-logging-1.0.4.jar
# https://repo.maven.apache.org/maven2/commons-codec/commons-codec/1.2/commons-codec-1.2.jar
# https://repo.maven.apache.org/maven2/junit/junit/3.8.1/junit-3.8.1.jar
Source1: %{name}-buildrequires-jars-%{version}.tar.gz

Source2: license.txt
%include %{SOURCE2}

Patch0: jakarta-commons-httpclient-encoding.patch
Patch1: 06_fix_CVE-2012-5783.patch
Patch2: CVE-2014-3577.patch
Patch3: CVE-2015-5262.patch

Requires: (openjdk11-jre or openjdk17-jre)

BuildRequires:  openjdk11
BuildRequires:  wget
BuildRequires:  apache-ant

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
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK*)
ant -Ddist.dir="." -Dbuild.sysclasspath=first -Dtest.failonerror=false \
        -Dlib.dir=./target/dependency -Djavac.encoding=UTF-8 dist

%install
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK*)
mkdir -p -m 755 %{buildroot}%{_prefix}
mkdir -p -m 755 %{buildroot}%{_datadir}/java/%{name}
cp -r dist/commons-httpclient.jar %{buildroot}%{_prefix}/
cp -r dist/commons-httpclient.jar %{buildroot}%{_datadir}/java/%{name}/

pushd %{buildroot}%{_prefix}
ln -s commons-httpclient.jar apache-commons-httpclient.jar
popd

pushd %{buildroot}%{_datadir}/java/%{name}
ln -s commons-httpclient.jar apache-commons-httpclient.jar
popd

cp -r dist/LICENSE.txt dist/README.txt %{buildroot}%{_prefix}/

%check
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK*)
ant -Ddist.dir="." -Dbuild.sysclasspath=first -Dtest.failonerror=false \
        -Dlib.dir=./target/dependency -Djavac.encoding=UTF-8 test

%files
%defattr(-,root,root)
%dir %{_prefix}
%{_prefix}/LICENSE.txt
%{_prefix}/README.txt
%{_prefix}/*.jar
%dir %{_datadir}/java/%{name}
%{_datadir}/java/%{name}/*.jar

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 3.1-6
- Release bump for SRP compliance
* Mon May 20 2024 Vamsi Krishna Brahmajosuyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.1-5
- Fix directory permissions
* Sat Aug 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.1-4
- Require jdk11 or jdk17
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.1-3
- Bump version as a part of openjdk11 upgrade
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 3.1-2
- Use openjdk11
* Thu Sep 10 2020 Ankit Jain <ankitja@vmware.com> 3.1-1
- Initial build. First version
