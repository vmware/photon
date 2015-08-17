%define _use_internal_dependency_generator 0
Summary:	OpenJDK 
Name:		openjdk
Version:	1.8.0.51
Release:	1%{?dist}
License:	GNU GPL
URL:		https://openjdk.java.net
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:   Photon
AutoReqProv: 	no
Source0:	http://anduin.linuxfromscratch.org/files/BLFS/OpenJDK-%{version}/OpenJDK-%{version}-x86_64-bin.tar.xz
%define sha1 OpenJDK=498263b52777406f02405ed610fa756f6b36f5df
%description
The OpenJDK package installs java class library and javac java compiler. 

%prep -p exit
%setup -qn OpenJDK-%{version}-x86_64-bin
%build

%install
install -vdm755 %{buildroot}/opt/OpenJDK-%{version}-bin 
mv -v %{_builddir}/OpenJDK-%{version}-x86_64-bin/* %{buildroot}/opt/OpenJDK-%{version}-bin/         
chown -R root:root %{buildroot}/opt/OpenJDK-%{version}-bin
install -vdm644 %{buildroot}/etc/profile.d

cat >> %{buildroot}/etc/profile.d/java-exports.sh <<- "EOF"
export CLASSPATH=.:/usr/share/java
export JAVA_HOME=/opt/OpenJDK-%{version}-bin
export PATH="$PATH:/opt/OpenJDK-1.8.0.51-bin/bin:/opt/OpenJDK-1.8.0.51-bin/jre/bin"
EOF

%clean
rm -rf %{buildroot}/*
%files
%defattr(-,root,root)
/opt/OpenJDK-%{version}-bin/*
/etc/profile.d/java-exports.sh
%changelog
*	Mon Aug 17 2015 Sharath George <sarahc@vmware.com> 1.8.0.51-1
-	Moved to the next version
*	Tue Jun 30 2015 Sarah Choi <sarahc@vmware.com> 1.8.0.45-2
-	Add JRE path 
*	Mon May 18 2015 Sharath George <sharathg@vmware.com> 1.8.0.45-1
-	Initial build.	First version
