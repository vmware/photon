%define _use_internal_dependency_generator 0
Summary:	OpenJDK 
Name:		openjdk
Version:	1.8.0.45
Release:	2%{?dist}
License:	GNU GPL
URL:		https://openjdk.java.net
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:   Photon
AutoReqProv: 	no
Source0:	http://anduin.linuxfromscratch.org/files/BLFS/OpenJDK-%{version}/OpenJDK-%{version}-x86_64-bin.tar.xz
%define sha1 OpenJDK=d9a073768d2ba66560ecccf46a5466d58ee0524f
%description
The OpenJDK package installs java class library and javac java compiler. 

%prep -p exit
%setup -qn OpenJDK-%{version}-bin
%build

%install
install -vdm755 %{buildroot}/opt/OpenJDK-%{version}-bin 
mv -v %{_builddir}/OpenJDK-%{version}-bin/* %{buildroot}/opt/OpenJDK-%{version}-bin/         
chown -R root:root %{buildroot}/opt/OpenJDK-%{version}-bin
install -vdm644 %{buildroot}/etc/profile.d

cat >> %{buildroot}/etc/profile.d/java-exports.sh <<- "EOF"
export CLASSPATH=.:/usr/share/java
export JAVA_HOME=/opt/OpenJDK-%{version}-bin
export PATH="$PATH:/opt/OpenJDK-1.8.0.45-bin/bin:/opt/OpenJDK-1.8.0.45-bin/jre/bin"
EOF

%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/opt/OpenJDK-%{version}-bin/*
/etc/profile.d/java-exports.sh
%changelog
*	Tue Jun 30 2015 Sarah Choi <sarahc@vmware.com> 1.8.0.45-2
-	Add JRE path 
*	Mon May 18 2015 Sharath George <sharathg@vmware.com> 1.8.0.45-1
-	Initial build.	First version
