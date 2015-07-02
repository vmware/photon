Summary:	Apache Maven
Name:		apache-maven
Version:	3.3.3
Release:	1%{?dist}
License:	Apache
URL:		http://maven.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://apache.mirrors.pair.com/maven/maven-3/%{version}/binaries/%{name}-%{version}-bin.tar.gz

Requires: 	openjdk >= 1.8.0.45
BuildRequires: 	openjdk >= 1.8.0.45

%description
The Maven package contains binaries for a build system

%prep

%setup -q
%build

%install

[ %{buildroot} != "/"] && rm -rf %{buildroot}/*

mkdir -p -m 700 %{buildroot}/opt
install -d -m 755 %{buildroot}/opt/%{name}
cp -R %{_builddir}/%{name}-%{version}/* %{buildroot}/opt/%{name}/

install -d -m 755 %{buildroot}/etc/profile.d/
echo 'export MAVEN_HOME=/opt/%{name}' > %{buildroot}/etc/profile.d/%{name}.sh
echo 'export PATH=$MAVEN_HOME/bin:$PATH' >> %{buildroot}/etc/profile.d/%{name}.sh
echo 'export MAVEN_OPTS=-Xms256m' >> %{buildroot}/etc/profile.d/%{name}.sh

%files
%defattr(-,root,root)
/opt/%{name}/*
/etc/profile.d/%{name}.sh

%changelog
*	Mon Jun 29 2015 Sarah Choi <sarahc@vmware.com> 3.3.3-1
-	Update PATH and remove unnecessary files
*	Fri May 22 2015 Sriram Nambakam <snambakam@vmware.com> 1.9.4
-	Initial build.	First version
