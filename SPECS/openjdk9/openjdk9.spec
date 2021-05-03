%define _use_internal_dependency_generator 0
%global security_hardening none
%define bootstrapjdkversion 1.8.0.112
%define jdk_major_version 1.9.0
%define subversion 181
Summary:	OpenJDK
Name:		openjdk9
Version:	%{jdk_major_version}.%{subversion}
Release:	4%{?dist}
License:	GNU GPL
URL:		https://openjdk.java.net
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:	http://www.java.net/download/openjdk/jdk9/b182/openjdk-%{version}.tar.gz
%define sha1 openjdk-1.9.0=0761abc2aabb0aa24f63ce96853ab3bb57ccce67
Patch0:         fix_jdk9_build_with_make4.3.patch
BuildRequires:  pcre-devel
BuildRequires:	which
BuildRequires:	zip
BuildRequires:	unzip
BuildRequires:  zlib-devel
BuildRequires:	ca-certificates
BuildRequires:	chkconfig
BuildRequires:  elfutils-libelf-devel
BuildRequires:  fontconfig-devel glib-devel harfbuzz-devel
BuildRequires:  freetype2 freetype2-devel
Requires:       openjre9 = %{version}-%{release}
Requires:       chkconfig
Obsoletes:      openjdk <= %{version}
Obsoletes:      openjdk-sample <= %{version}
Obsoletes:      openjdk-src <= %{version}
Obsoletes:      openjdk-doc <= %{version}
AutoReqProv: 	no
%description
The OpenJDK package installs java class library and javac java compiler.

%package	-n openjre9
Summary:	Java runtime environment
AutoReqProv: 	no
Obsoletes:      openjre <= %{version}
Requires:       chkconfig
Requires:	libstdc++
%description	-n openjre9
It contains the libraries files for Java runtime environment

%package		doc
Summary:		Documentation and demo applications for openjdk
Group:          Development/Languages/Java
Obsoletes:      openjdk-doc <= %{version}
Requires:       %{name} = %{version}-%{release}
%description	doc
It contains the documentation and demo applications for openjdk

%package 		src
Summary:        OpenJDK Java classes for developers
Group:          Development/Languages/Java
Obsoletes:      openjdk-src <= %{version}
Requires:       %{name} = %{version}-%{release}
%description	src
This package provides the runtime library class sources.

%prep -p exit
%setup -qn openjdk-%{version}
%patch0 -p1

%build
chmod a+x ./configure
unset JAVA_HOME &&
ENABLE_HEADLESS_ONLY="true" &&
./configure \
	--with-target-bits=64 \
	--with-boot-jdk=/var/opt/OpenJDK-%bootstrapjdkversion-bin \
	--enable-headless-only \
        --with-extra-cxxflags="-Wno-error -std=gnu++98 -fno-delete-null-pointer-checks -fno-lifetime-dse" \
	--with-extra-cflags="-fno-delete-null-pointer-checks -Wno-error -fno-lifetime-dse" \
	--with-freetype-include=/usr/include/freetype2 \
	--with-freetype-lib=/usr/lib \
	--with-stdc++lib=dynamic \
        --disable-warnings-as-errors

mkdir /usr/share/java -p
make \
    DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
    SCTP_WERROR= \
    BUILD_HEADLESS_ONLY=1 \
    OPENJDK_TARGET_OS=linux \
    STRIP_POLICY=no_strip \
    POST_STRIP_CMD="" \
    LOG=trace

%install
unset JAVA_HOME &&
make DESTDIR=%{buildroot} install \
	BUILD_HEADLESS_ONLY=yes \
	OPENJDK_TARGET_OS=linux \
	DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
	CLASSPATH=/var/opt/OpenJDK-%bootstrapjdkversion-bin/jre

install -vdm755 %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}
chown -R root:root %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}
install -vdm755 %{buildroot}%{_bindir}
mv /usr/local/jvm/openjdk-9-internal/* %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/
mv build/linux-x86_64-normal-server-release/images/jre %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/
cp README LICENSE ASSEMBLY_EXCEPTION %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/

%posttrans
alternatives --install %{_bindir}/javac javac %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javac 2000 \
  --slave %{_bindir}/appletviewer appletviewer %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/appletviewer \
  --slave %{_bindir}/idlj idlj %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/idlj \
  --slave %{_bindir}/jaotc jaotc %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jaotc \
  --slave %{_bindir}/jar jar %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jar \
  --slave %{_bindir}/jarsigner jarsigner %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jarsigner \
  --slave %{_bindir}/jhsdb jhsdb %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jhsdb \
  --slave %{_bindir}/jimage jimage %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jimage \
  --slave %{_bindir}/jlink jlink %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jlink \
  --slave %{_bindir}/jmod jmod %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jmod \
  --slave %{_bindir}/javadoc javadoc %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javadoc \
  --slave %{_bindir}/javah javah %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javah \
  --slave %{_bindir}/javap javap %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javap \
  --slave %{_bindir}/jcmd jcmd %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jcmd \
  --slave %{_bindir}/jdeprscan jdeprscan %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jdeprscan \
  --slave %{_bindir}/jconsole jconsole %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jconsole \
  --slave %{_bindir}/jdb jdb %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jdb \
  --slave %{_bindir}/jdeps jdeps %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jdeps \
  --slave %{_bindir}/jinfo jinfo %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jinfo \
  --slave %{_bindir}/jmap jmap %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jmap \
  --slave %{_bindir}/jps jps %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jps \
  --slave %{_bindir}/jrunscript jrunscript %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jrunscript \
  --slave %{_bindir}/jstack jstack %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jstack \
  --slave %{_bindir}/jstat jstat %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jstat \
  --slave %{_bindir}/jstatd jstatd %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jstatd \
  --slave %{_bindir}/rmic rmic %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/rmic \
  --slave %{_bindir}/schemagen schemagen %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/schemagen \
  --slave %{_bindir}/serialver serialver %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/serialver \
  --slave %{_bindir}/wsgen wsgen %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/wsgen \
  --slave %{_bindir}/wsimport wsimport %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/wsimport \
  --slave %{_bindir}/xjc xjc %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/xjc
/sbin/ldconfig

%posttrans -n openjre9
alternatives --install %{_bindir}/java java %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jre/bin/java 2000 \
  --slave %{_libdir}/jvm/jre jre %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jre \
  --slave %{_bindir}/jjs jjs %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jre/bin/jjs \
  --slave %{_bindir}/keytool keytool %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jre/bin/keytool \
  --slave %{_bindir}/orbd orbd %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jre/bin/orbd \
  --slave %{_bindir}/pack200 pack200 %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jre/bin/pack200 \
  --slave %{_bindir}/rmid rmid %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jre/bin/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jre/bin/rmiregistry \
  --slave %{_bindir}/servertool servertool %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jre/bin/servertool \
  --slave %{_bindir}/tnameserv tnameserv %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jre/bin/tnameserv \
  --slave %{_bindir}/unpack200 unpack200 %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jre/bin/unpack200
/sbin/ldconfig

%postun
alternatives --remove javac %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javac
/sbin/ldconfig

%postun -n openjre9
alternatives --remove java %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jre/bin/java
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*
rm -rf %{_libdir}/jvm/OpenJDK-*

%files
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/ASSEMBLY_EXCEPTION
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/LICENSE
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/README
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/release
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/lib
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/include/
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/idlj
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jaotc
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jar
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jhsdb
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jimage
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jarsigner
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jdeprscan
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javac
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javadoc
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javah
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javap
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jcmd
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jconsole
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jdb
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jdeps
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jinfo
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jlink
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jmod
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jmap
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jps
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jshell
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jrunscript
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jstack
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jstat
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jstatd
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/rmic
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/schemagen
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/serialver
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/wsgen
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/wsimport
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/xjc
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/conf
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jmods

%files	-n openjre9
%defattr(-,root,root)
%dir %{_libdir}/jvm/OpenJDK-%{jdk_major_version}
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jre/
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/java
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/keytool
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/orbd
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/pack200
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jjs
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/rmid
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/rmiregistry
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/servertool
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/tnameserv
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/unpack200

%files doc
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/man/
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/legal/
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/demo

%files src
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/lib/src.zip

%changelog
*   Mon May 24 2021 Tapas Kundu <tkundu@vmware.com> 1.9.0.181-4
-   Fix build with make 4.3
*   Tue Aug 11 2020 Ankit Jain <ankitja@vmware.com> 1.9.0.181-3
-   Replaced %post to %posttrans to avoid alternatives --remove
-   after new version is installed.
*   Fri Jul 26 2019 Ankit Jain <ankitja@vmware.com> 1.9.0.181-2
-   Divided version:majorversion+subversion to remove specific
-   version java dependency from other packages
*   Fri Jul 20 2018 Tapas Kundu <tkundu@vmware.com> 1.9.0.181-1
-   Initial build. First version
