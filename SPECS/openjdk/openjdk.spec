%define _use_internal_dependency_generator 0
Summary:	OpenJDK 
Name:		openjdk
Version:	1.8.0.51
Release:	3%{?dist}
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

%package	-n openjre
Summary:	Jave runtime environtment
AutoReqProv: 	no
%description	-n openjre
It contains the libraries files for Java runtime environment
#%global __requires_exclude ^libgif.*$
#%filter_from_requires ^libgif.*$

%package		sample
Summary:		Sample java applications. 
Group:          Development/Languages/Java
%description	sample
It contains the Sample java applications.
Requires:       %{name} = %{version}

%package		doc
Summary:		Documentation and demo applications for openjdk
Group:          Development/Languages/Java
%description	doc
It contains the documentation and demo applications for openjdk
Requires:       %{name} = %{version}-%{release}

%package 		src
Summary:        OpenJDK Java classes for developers
Group:          Development/Languages/Java
%description	src
This package provides the runtime library class sources. 
Requires:       %{name} = %{version}

%prep -p exit
%setup -qn OpenJDK-%{version}-x86_64-bin
%build

%install
install -vdm755 %{buildroot}/var/opt/OpenJDK-%{version}-bin 
mv -v %{_builddir}/OpenJDK-%{version}-x86_64-bin/* %{buildroot}/var/opt/OpenJDK-%{version}-bin/         
chown -R root:root %{buildroot}/var/opt/OpenJDK-%{version}-bin
install -vdm644 %{buildroot}/etc/profile.d

cat >> %{buildroot}/etc/profile.d/java-exports.sh <<- "EOF"
export CLASSPATH=.:/usr/share/java
export JAVA_HOME=/var/opt/OpenJDK-%{version}-bin
export PATH="$PATH:/var/opt/OpenJDK-%{version}-bin/bin:/var/opt/OpenJDK-%{version}-bin/jre/bin"
EOF

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
/var/opt/OpenJDK-%{version}-bin/ASSEMBLY_EXCEPTION
/var/opt/OpenJDK-%{version}-bin/LICENSE
/var/opt/OpenJDK-%{version}-bin/release
/var/opt/OpenJDK-%{version}-bin/THIRD_PARTY_README
/var/opt/OpenJDK-%{version}-bin/lib
/var/opt/OpenJDK-%{version}-bin/include/

%files	-n openjre
%defattr(-,root,root)
/var/opt/OpenJDK-%{version}-bin/jre/ 
/var/opt/OpenJDK-%{version}-bin/bin
/var/opt/OpenJDK-%{version}-bin/lib/amd64/jli/
/etc/profile.d/java-exports.sh

%files sample
%defattr(-,root,root)
/var/opt/OpenJDK-%{version}-bin/sample/

%files doc
%defattr(-,root,root)
/var/opt/OpenJDK-%{version}-bin/man/
/var/opt/OpenJDK-%{version}-bin/demo

%files src
%defattr(-,root,root)
/var/opt/OpenJDK-%{version}-bin/src.zip

%changelog
*	Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 1.8.0.51-3
-	Change to use /var/opt path
*	Fri Sep 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.0.51-2
-	Split the openjdk into multiple sub-packages to reduce size. 
*	Mon Aug 17 2015 Sharath George <sarahc@vmware.com> 1.8.0.51-1
-	Moved to the next version
*	Tue Jun 30 2015 Sarah Choi <sarahc@vmware.com> 1.8.0.45-2
-	Add JRE path 
*	Mon May 18 2015 Sharath George <sharathg@vmware.com> 1.8.0.45-1
-	Initial build.	First version
