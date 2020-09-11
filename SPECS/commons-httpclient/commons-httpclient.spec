Summary:	Apache commons-httpclient
Name:		commons-httpclient
Version:	3.1
Release:	1%{?dist}
License:	Apache
URL:		http://ant.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      noarch
Source0:	https://archive.apache.org/dist/httpcomponents/%{name}/source/%{name}-%{version}-src.tar.gz
%define sha1 commons-httpclient=5c604f102e0716597b3d2659ac3e77f80a02f22d
# Bundled below jar into tarball
# https://repo.maven.apache.org/maven2/commons-logging/commons-logging/1.0.4/commons-logging-1.0.4.jar
# https://repo.maven.apache.org/maven2/commons-codec/commons-codec/1.2/commons-codec-1.2.jar
# https://repo.maven.apache.org/maven2/junit/junit/3.8.1/junit-3.8.1.jar
Source1:        %{name}-buildrequires-jars-%{version}.tar.gz
%define sha1 commons-httpclient-buildrequires-jars=8936aa9af8be604a89691ebfca0c7b000dc50c3c
Patch0:         jakarta-commons-httpclient-encoding.patch
Patch1:         06_fix_CVE-2012-5783.patch
Patch2:         CVE-2014-3577.patch
Patch3:         CVE-2015-5262.patch
Requires:       openjre8
BuildRequires:  wget
BuildRequires:  openjre8
BuildRequires:  openjdk8
BuildRequires:  apache-ant
%define _prefix /var/opt/%{name}

%description
The Hyper-Text Transfer Protocol (HTTP) is perhaps the most significant
protocol used on the Internet today. Web services, network-enabled
appliances and the growth of network computing continue to expand the
role of the HTTP protocol beyond user-driven web browsers, while
increasing the number of applications that require HTTP support.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

mkdir -p target/dependency
tar -xf %{SOURCE1} -C target/dependency --no-same-owner
pushd target/dependency
cp %{name}-buildrequires-jars-%{version}/*.jar .
popd

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
ant -Ddist.dir="." -Dbuild.sysclasspath=first -Dtest.failonerror=false -Dlib.dir=./target/dependency -Djavac.encoding=UTF-8 dist

%install
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
mkdir -p -m 700 %{buildroot}%{_prefix}
mkdir -p -m 700 %{buildroot}%{_datadir}/java/%{name}
cp -r dist/commons-httpclient.jar %{buildroot}%{_prefix}/
cp -r dist/commons-httpclient.jar %{buildroot}%{_datadir}/java/%{name}/
pushd %{buildroot}%{_prefix}
ln -s commons-httpclient.jar apache-commons-httpclient.jar
popd
pushd %{buildroot}%{_datadir}/java/%{name}
ln -s commons-httpclient.jar apache-commons-httpclient.jar
popd

cp -r dist/LICENSE.txt %{buildroot}%{_prefix}/
cp -r dist/README.txt %{buildroot}%{_prefix}/

%check
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
ant -Ddist.dir="." -Dbuild.sysclasspath=first -Dtest.failonerror=false -Dlib.dir=./target/dependency -Djavac.encoding=UTF-8 test

%files
%defattr(-,root,root)
%dir %{_prefix}
%{_prefix}/LICENSE.txt
%{_prefix}/README.txt
%{_prefix}/*.jar
%dir %{_datadir}/java/%{name}
%{_datadir}/java/%{name}/*.jar

%changelog
*   Thu Sep 10 2020 Ankit Jain <ankitja@vmware.com> 3.1-1
-   Initial build. First version
