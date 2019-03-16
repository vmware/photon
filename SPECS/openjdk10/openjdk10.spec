%define _use_internal_dependency_generator 0
%global security_hardening none
Summary:	OpenJDK
Name:		openjdk10
Version:	1.10.0.23
Release:	3%{?dist}
License:	GNU GPL
URL:		https://openjdk.java.net
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:	http://www.java.net/download/openjdk/jdk10/jdk10/openjdk-%{version}.tar.gz
%define sha1 openjdk-1.10.0=d0b6193fd1687b23fb7553b62d32f0e7e0527ea8
BuildRequires:  pcre-devel
BuildRequires:	which
BuildRequires:	zip
BuildRequires:	unzip
BuildRequires:  zlib-devel
BuildRequires:	ca-certificates
BuildRequires:	chkconfig
BuildRequires:  fontconfig-devel freetype2-devel glib-devel harfbuzz-devel elfutils-libelf-devel
Requires:       openjre10 = %{version}-%{release}
Requires:       chkconfig
AutoReqProv: 	no
%define ExtraBuildRequires icu-devel, cups, cups-devel, xorg-proto-devel, libXtst, libXtst-devel, libXfixes, libXfixes-devel, libXi, libXi-devel, openjdk, openjre, icu, alsa-lib, alsa-lib-devel, xcb-proto, libXdmcp-devel, libXau-devel, util-macros, xtrans, libxcb-devel, proto, libXdmcp,libxcb, libXau, xtrans-devel, libX11, libX11-devel, libXext, libXext-devel, libICE-devel, libSM, libICE, libSM-devel, libXt, libXmu, libXt-devel,libXmu-devel, libXrender, libXrender-devel
%define bootstrapjdkversion 1.8.0.112
%define jdk_major_version 1.10.0
%description
The OpenJDK package installs java class library and javac java compiler.

%package	-n openjre10
Summary:	Java runtime environment
AutoReqProv: 	no
Requires:       chkconfig
Requires:	libstdc++
%description	-n openjre10
It contains the libraries files for Java runtime environment

%package		doc
Summary:		Documentation and demo applications for openjdk
Group:          Development/Languages/Java
Requires:       %{name} = %{version}-%{release}
%description	doc
It contains the documentation and demo applications for openjdk

%package 		src
Summary:        OpenJDK Java classes for developers
Group:          Development/Languages/Java
Requires:       %{name} = %{version}-%{release}
%description	src
This package provides the runtime library class sources.

%prep -p exit
%setup -qn openjdk-%{version}

%build
chmod a+x ./configure
unset JAVA_HOME &&
ENABLE_HEADLESS_ONLY="true" &&
sh configure \
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
make install

install -vdm755 %{buildroot}%{_libdir}/jvm/OpenJDK-%{version}
chown -R root:root %{buildroot}%{_libdir}/jvm/OpenJDK-%{version}
install -vdm755 %{buildroot}%{_bindir}
mv /usr/local/jvm/openjdk-10-internal/* %{buildroot}%{_libdir}/jvm/OpenJDK-%{version}/
mv build/linux-x86_64-normal-server-release/images/jre %{buildroot}%{_libdir}/jvm/OpenJDK-%{version}/
cp README LICENSE ASSEMBLY_EXCEPTION %{buildroot}%{_libdir}/jvm/OpenJDK-%{version}/

%post
alternatives --install %{_bindir}/javac javac %{_libdir}/jvm/OpenJDK-%{version}/bin/javac 2000 \
  --slave %{_bindir}/appletviewer appletviewer %{_libdir}/jvm/OpenJDK-%{version}/bin/appletviewer \
  --slave %{_bindir}/idlj idlj %{_libdir}/jvm/OpenJDK-%{version}/bin/idlj \
  --slave %{_bindir}/jaotc jaotc %{_libdir}/jvm/OpenJDK-%{version}/bin/jaotc \
  --slave %{_bindir}/jar jar %{_libdir}/jvm/OpenJDK-%{version}/bin/jar \
  --slave %{_bindir}/jarsigner jarsigner %{_libdir}/jvm/OpenJDK-%{version}/bin/jarsigner \
  --slave %{_bindir}/jhsdb jhsdb %{_libdir}/jvm/OpenJDK-%{version}/bin/jhsdb \
  --slave %{_bindir}/jimage jimage %{_libdir}/jvm/OpenJDK-%{version}/bin/jimage \
  --slave %{_bindir}/jlink jlink %{_libdir}/jvm/OpenJDK-%{version}/bin/jlink \
  --slave %{_bindir}/jmod jmod %{_libdir}/jvm/OpenJDK-%{version}/bin/jmod \
  --slave %{_bindir}/javadoc javadoc %{_libdir}/jvm/OpenJDK-%{version}/bin/javadoc \
  --slave %{_bindir}/javah javah %{_libdir}/jvm/OpenJDK-%{version}/bin/javah \
  --slave %{_bindir}/javap javap %{_libdir}/jvm/OpenJDK-%{version}/bin/javap \
  --slave %{_bindir}/jcmd jcmd %{_libdir}/jvm/OpenJDK-%{version}/bin/jcmd \
  --slave %{_bindir}/jdeprscan jdeprscan %{_libdir}/jvm/OpenJDK-%{version}/bin/jdeprscan \
  --slave %{_bindir}/jconsole jconsole %{_libdir}/jvm/OpenJDK-%{version}/bin/jconsole \
  --slave %{_bindir}/jdb jdb %{_libdir}/jvm/OpenJDK-%{version}/bin/jdb \
  --slave %{_bindir}/jdeps jdeps %{_libdir}/jvm/OpenJDK-%{version}/bin/jdeps \
  --slave %{_bindir}/jinfo jinfo %{_libdir}/jvm/OpenJDK-%{version}/bin/jinfo \
  --slave %{_bindir}/jmap jmap %{_libdir}/jvm/OpenJDK-%{version}/bin/jmap \
  --slave %{_bindir}/jps jps %{_libdir}/jvm/OpenJDK-%{version}/bin/jps \
  --slave %{_bindir}/jrunscript jrunscript %{_libdir}/jvm/OpenJDK-%{version}/bin/jrunscript \
  --slave %{_bindir}/jstack jstack %{_libdir}/jvm/OpenJDK-%{version}/bin/jstack \
  --slave %{_bindir}/jstat jstat %{_libdir}/jvm/OpenJDK-%{version}/bin/jstat \
  --slave %{_bindir}/jstatd jstatd %{_libdir}/jvm/OpenJDK-%{version}/bin/jstatd \
  --slave %{_bindir}/rmic rmic %{_libdir}/jvm/OpenJDK-%{version}/bin/rmic \
  --slave %{_bindir}/schemagen schemagen %{_libdir}/jvm/OpenJDK-%{version}/bin/schemagen \
  --slave %{_bindir}/serialver serialver %{_libdir}/jvm/OpenJDK-%{version}/bin/serialver \
  --slave %{_bindir}/wsgen wsgen %{_libdir}/jvm/OpenJDK-%{version}/bin/wsgen \
  --slave %{_bindir}/wsimport wsimport %{_libdir}/jvm/OpenJDK-%{version}/bin/wsimport \
  --slave %{_bindir}/xjc xjc %{_libdir}/jvm/OpenJDK-%{version}/bin/xjc
/sbin/ldconfig

%post -n openjre10
alternatives --install %{_bindir}/java java %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/java 2000 \
  --slave %{_libdir}/jvm/jre jre %{_libdir}/jvm/OpenJDK-%{version}/jre \
  --slave %{_bindir}/jjs jjs %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/jjs \
  --slave %{_bindir}/keytool keytool %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/keytool \
  --slave %{_bindir}/orbd orbd %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/orbd \
  --slave %{_bindir}/pack200 pack200 %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/pack200 \
  --slave %{_bindir}/rmid rmid %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/rmiregistry \
  --slave %{_bindir}/servertool servertool %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/servertool \
  --slave %{_bindir}/tnameserv tnameserv %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/tnameserv \
  --slave %{_bindir}/unpack200 unpack200 %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/unpack200
/sbin/ldconfig

%postun
alternatives --remove javac %{_libdir}/jvm/OpenJDK-%{version}/bin/javac
/sbin/ldconfig

%postun -n openjre10
alternatives --remove java %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/java
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*
rm -rf %{_libdir}/jvm/OpenJDK-*

%files
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{version}/ASSEMBLY_EXCEPTION
%{_libdir}/jvm/OpenJDK-%{version}/LICENSE
%{_libdir}/jvm/OpenJDK-%{version}/README
%{_libdir}/jvm/OpenJDK-%{version}/release
%{_libdir}/jvm/OpenJDK-%{version}/lib
%{_libdir}/jvm/OpenJDK-%{version}/include/
%{_libdir}/jvm/OpenJDK-%{version}/bin/idlj
%{_libdir}/jvm/OpenJDK-%{version}/bin/jaotc
%{_libdir}/jvm/OpenJDK-%{version}/bin/jar
%{_libdir}/jvm/OpenJDK-%{version}/bin/jhsdb
%{_libdir}/jvm/OpenJDK-%{version}/bin/jimage
%{_libdir}/jvm/OpenJDK-%{version}/bin/jarsigner
%{_libdir}/jvm/OpenJDK-%{version}/bin/jdeprscan
%{_libdir}/jvm/OpenJDK-%{version}/bin/javac
%{_libdir}/jvm/OpenJDK-%{version}/bin/javadoc
%{_libdir}/jvm/OpenJDK-%{version}/bin/javah
%{_libdir}/jvm/OpenJDK-%{version}/bin/javap
%{_libdir}/jvm/OpenJDK-%{version}/bin/jcmd
%{_libdir}/jvm/OpenJDK-%{version}/bin/jconsole
%{_libdir}/jvm/OpenJDK-%{version}/bin/jdb
%{_libdir}/jvm/OpenJDK-%{version}/bin/jdeps
%{_libdir}/jvm/OpenJDK-%{version}/bin/jinfo
%{_libdir}/jvm/OpenJDK-%{version}/bin/jlink
%{_libdir}/jvm/OpenJDK-%{version}/bin/jmod
%{_libdir}/jvm/OpenJDK-%{version}/bin/jmap
%{_libdir}/jvm/OpenJDK-%{version}/bin/jps
%{_libdir}/jvm/OpenJDK-%{version}/bin/jshell
%{_libdir}/jvm/OpenJDK-%{version}/bin/jrunscript
%{_libdir}/jvm/OpenJDK-%{version}/bin/jstack
%{_libdir}/jvm/OpenJDK-%{version}/bin/jstat
%{_libdir}/jvm/OpenJDK-%{version}/bin/jstatd
%{_libdir}/jvm/OpenJDK-%{version}/bin/rmic
%{_libdir}/jvm/OpenJDK-%{version}/bin/schemagen
%{_libdir}/jvm/OpenJDK-%{version}/bin/serialver
%{_libdir}/jvm/OpenJDK-%{version}/bin/wsgen
%{_libdir}/jvm/OpenJDK-%{version}/bin/wsimport
%{_libdir}/jvm/OpenJDK-%{version}/bin/xjc
%{_libdir}/jvm/OpenJDK-%{version}/conf
%{_libdir}/jvm/OpenJDK-%{version}/jmods

%files	-n openjre10
%defattr(-,root,root)
%dir %{_libdir}/jvm/OpenJDK-%{version}
%{_libdir}/jvm/OpenJDK-%{version}/jre/
%{_libdir}/jvm/OpenJDK-%{version}/bin/java
%{_libdir}/jvm/OpenJDK-%{version}/bin/keytool
%{_libdir}/jvm/OpenJDK-%{version}/bin/orbd
%{_libdir}/jvm/OpenJDK-%{version}/bin/pack200
%{_libdir}/jvm/OpenJDK-%{version}/bin/jjs
%{_libdir}/jvm/OpenJDK-%{version}/bin/rmid
%{_libdir}/jvm/OpenJDK-%{version}/bin/rmiregistry
%{_libdir}/jvm/OpenJDK-%{version}/bin/servertool
%{_libdir}/jvm/OpenJDK-%{version}/bin/tnameserv
%{_libdir}/jvm/OpenJDK-%{version}/bin/unpack200

%files doc
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{version}/man/
%{_libdir}/jvm/OpenJDK-%{version}/legal/
%{_libdir}/jvm/OpenJDK-%{version}/demo

%files src
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{version}/lib/src.zip

%changelog
*   Fri Mar 15 2019 Ankit Jain <ankitja@vmware.com> 1.10.0.23-3
-   Added ExtraBuildRequires macro
*   Tue Jul 31 2018 Tapas Kundu <tkundu@vmware.com> 1.10.0.23-2
-   Removed installing openjdk9 with openjdk10 and removed obsolete for openjdk.
*   Mon Jul 16 2018 Tapas Kundu <tkundu@vmware.com> 1.10.0.23-1
-   Initial build. First version
