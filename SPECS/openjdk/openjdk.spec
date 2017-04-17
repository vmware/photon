%define _use_internal_dependency_generator 0
%global security_hardening none
Summary:	OpenJDK 
Name:		openjdk
Version:	1.8.0.131
Release:	1%{?dist}
License:	GNU GPL
URL:		https://openjdk.java.net
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:	http://anduin.linuxfromscratch.org/files/BLFS/OpenJDK/openjdk-%{version}.tar.bz2
%define sha1 openjdk=ae01c24fe5247d5aa246a60c0272ba92188a7d55
Source1:    macros.java
Patch0:		disable-awt-lib.patch
Patch1:		fix-lcms.patch 
Patch2:		Fix-memory-leak.patch
Patch3:		check-system-ca-certs.patch
BuildRequires:  pcre-devel
BuildRequires:	which
BuildRequires:	zip
BuildRequires:	unzip
BuildRequires:  zlib-devel
BuildRequires:	ca-certificates
Requires:       openjre = %{version}-%{release}
AutoReqProv: 	no
%define bootstrapjdkversion 1.8.0.112
%description
The OpenJDK package installs java class library and javac java compiler. 

%package	-n openjre
Summary:	Java runtime environment
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
Requires:       %{name} = %{version}-%{release}

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
Requires:       %{name} = %{version}-%{release}

%prep -p exit
%setup -q -n openjdk
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
chmod a+x ./configure
unset JAVA_HOME &&
./configure \
	FREETYPE_NOT_NEEDED=yes \
	CUPS_NOT_NEEDED=yes \
	--with-target-bits=64 \
	--with-boot-jdk=/var/opt/OpenJDK-%bootstrapjdkversion-bin \
	--enable-headful=no \
	--with-cacerts-file=/var/opt/OpenJDK-%bootstrapjdkversion-bin/jre/lib/security/cacerts \
	--with-extra-cxxflags="-Wno-error -std=gnu++98 -fno-delete-null-pointer-checks -fno-lifetime-dse" \
	--with-extra-cflags="-std=gnu++98 -fno-delete-null-pointer-checks -Wno-error -fno-lifetime-dse" \
	--with-stdc++lib=dynamic

make \
    DEBUG_BINARIES=true \
    BUILD_HEADLESS_ONLY=yes \
    OPENJDK_TARGET_OS=linux \
    JAVAC_FLAGS=-g \
    STRIP_POLICY=no_strip \
    DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
    CLASSPATH=/var/opt/OpenJDK-%bootstrapjdkversion-bin/jre \
    POST_STRIP_CMD="" \
    LOG=trace \
    SCTP_WERROR=

%install
make DESTDIR=%{buildroot} install \
	BUILD_HEADLESS_ONLY=yes \
	OPENJDK_TARGET_OS=linux \
	DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
	CLASSPATH=/var/opt/OpenJDK-%bootstrapjdkversion-bin/jre

install -vdm755 %{buildroot}/var/opt/OpenJDK-%{version}-bin
chown -R root:root %{buildroot}/var/opt/OpenJDK-%{version}-bin
mkdir -p %{buildroot}/etc/profile.d
install -vdm755 %{buildroot}%{_rpmconfigdir}/macros.d
install -m 644 %{SOURCE1} %{buildroot}/%{_rpmconfigdir}/macros.d/
install -vdm644 %{buildroot}/etc/profile.d
mv /usr/local/jvm/openjdk-1.8.0-internal/* %{buildroot}/var/opt/OpenJDK-%{version}-bin/

cat >> %{buildroot}/etc/profile.d/java-exports.sh <<- "EOF"
export CLASSPATH=.:/usr/share/java
export JAVA_HOME=/var/opt/OpenJDK-%{version}-bin
export PATH="$PATH:/var/opt/OpenJDK-%{version}-bin/bin:/var/opt/OpenJDK-%{version}-bin/jre/bin"
EOF

chmod a+x %{buildroot}/etc/profile.d/java-exports.sh

%post
source /etc/profile.d/java-exports.sh

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
/var/opt/OpenJDK-%{version}-bin/bin/extcheck
/var/opt/OpenJDK-%{version}-bin/bin/idlj
/var/opt/OpenJDK-%{version}-bin/bin/jar
/var/opt/OpenJDK-%{version}-bin/bin/jarsigner
/var/opt/OpenJDK-%{version}-bin/bin/java-rmi.cgi
/var/opt/OpenJDK-%{version}-bin/bin/javac
/var/opt/OpenJDK-%{version}-bin/bin/javadoc
/var/opt/OpenJDK-%{version}-bin/bin/javah
/var/opt/OpenJDK-%{version}-bin/bin/javap
/var/opt/OpenJDK-%{version}-bin/bin/jcmd
/var/opt/OpenJDK-%{version}-bin/bin/jconsole
/var/opt/OpenJDK-%{version}-bin/bin/jdb
/var/opt/OpenJDK-%{version}-bin/bin/jdeps
/var/opt/OpenJDK-%{version}-bin/bin/jhat
/var/opt/OpenJDK-%{version}-bin/bin/jinfo
/var/opt/OpenJDK-%{version}-bin/bin/jjs
/var/opt/OpenJDK-%{version}-bin/bin/jmap
/var/opt/OpenJDK-%{version}-bin/bin/jps
/var/opt/OpenJDK-%{version}-bin/bin/jrunscript
/var/opt/OpenJDK-%{version}-bin/bin/jsadebugd
/var/opt/OpenJDK-%{version}-bin/bin/jstack
/var/opt/OpenJDK-%{version}-bin/bin/jstat
/var/opt/OpenJDK-%{version}-bin/bin/jstatd
/var/opt/OpenJDK-%{version}-bin/bin/native2ascii
/var/opt/OpenJDK-%{version}-bin/bin/rmic
/var/opt/OpenJDK-%{version}-bin/bin/schemagen
/var/opt/OpenJDK-%{version}-bin/bin/serialver
/var/opt/OpenJDK-%{version}-bin/bin/wsgen
/var/opt/OpenJDK-%{version}-bin/bin/wsimport
/var/opt/OpenJDK-%{version}-bin/bin/xjc


%files	-n openjre
%defattr(-,root,root)

/var/opt/OpenJDK-%{version}-bin/jre/
/var/opt/OpenJDK-%{version}-bin/bin/java
/var/opt/OpenJDK-%{version}-bin/bin/keytool
/var/opt/OpenJDK-%{version}-bin/bin/orbd
/var/opt/OpenJDK-%{version}-bin/bin/pack200
/var/opt/OpenJDK-%{version}-bin/bin/rmid
/var/opt/OpenJDK-%{version}-bin/bin/rmiregistry
/var/opt/OpenJDK-%{version}-bin/bin/servertool
/var/opt/OpenJDK-%{version}-bin/bin/tnameserv
/var/opt/OpenJDK-%{version}-bin/bin/unpack200
/var/opt/OpenJDK-%{version}-bin/lib/amd64/jli/
/etc/profile.d/java-exports.sh
%{_rpmconfigdir}/macros.d/macros.java

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
*	Mon Apr 10 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.0.131-1
-	Upgraded to version 1.8.0.131 and building Java from sources
*       Tue Mar 28 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.0.112-2
-       add java rpm macros
*       Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.0.112-1
-       Update to 1.8.0.112. addresses CVE-2016-5582 CVE-2016-5573
*       Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.0.102-1
-       Update to 1.8.0.102, minor fixes in url, spelling.
-       addresses CVE-2016-3598, CVE-2016-3606, CVE-2016-3610
*       Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com> 1.8.0.92-3
-	Added version constraint to runtime dependencies
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.0.92-2
-	GA - Bump release of all rpms
*       Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 1.8.0.92-1
-	Updated to version 1.8.0.92
*       Mon May 2 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.0.72-3
-       Move tools like javac to openjdk
*       Thu Apr 28 2016 Divya Thaluru <dthaluru@vmware.com> 1.8.0.72-2
-       Adding openjre as run time dependency for openjdk package
*       Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.8.0.72-1
-       Updating Version.
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
