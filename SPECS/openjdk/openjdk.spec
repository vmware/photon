%define _use_internal_dependency_generator 0
Summary:	OpenJDK 
Name:		openjdk
Version:	1.8.0.45
Release:	1%{?dist}
License:	GNU GPL
URL:		https://openjdk.java.net
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:   Photon
AutoReqProv: 	no
Source0:	http://anduin.linuxfromscratch.org/files/BLFS/OpenJDK-%{version}/OpenJDK-%{version}-x86_64-bin.tar.xz
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
export PATH="$PATH:/opt/OpenJDK-1.8.0.45-bin/bin"
EOF

%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/opt/OpenJDK-%{version}-bin/*
/etc/profile.d/java-exports.sh
%changelog
*	Mon May 18 2015 Sharath George <sharathg@vmware.com> 1.8.0.45-1
-	Initial build.	First version
