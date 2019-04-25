%define _use_internal_dependency_generator 0
%global security_hardening none
%define jdk_major_version 1.11.0
Summary:	OpenJDK
Name:		openjdk11
Version:	1.11.0.2
Release:	2%{?dist}
License:	GNU General Public License V2
URL:		https://openjdk.java.net
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:	http://www.java.net/download/openjdk/jdk/jdk11/openjdk-%{version}.tar.gz
%define sha1 openjdk-1.11.0=aa24e47c3e67c3ef6c7eceaebb21123a67ab8fea
BuildRequires:  pcre-devel
BuildRequires:	which
BuildRequires:	zip
BuildRequires:	unzip
BuildRequires:  zlib-devel
BuildRequires:	ca-certificates
BuildRequires:	chkconfig
BuildRequires:  freetype2
BuildRequires:  fontconfig-devel freetype2-devel glib-devel harfbuzz-devel elfutils-libelf-devel
BuildRequires:  openjdk10
Requires:       chkconfig
AutoReqProv: 	no
%description
The OpenJDK package installs java class library and javac java compiler.

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
./configure \
	--with-target-bits=64 \
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
mv /usr/local/jvm/openjdk-11-internal/* %{buildroot}%{_libdir}/jvm/OpenJDK-%{version}/
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

%postun
alternatives --remove javac %{_libdir}/jvm/OpenJDK-%{version}/bin/javac
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
%{_libdir}/jvm/OpenJDK-%{version}/bin/jaotc
%{_libdir}/jvm/OpenJDK-%{version}/bin/jar
%{_libdir}/jvm/OpenJDK-%{version}/bin/jhsdb
%{_libdir}/jvm/OpenJDK-%{version}/bin/jimage
%{_libdir}/jvm/OpenJDK-%{version}/bin/jarsigner
%{_libdir}/jvm/OpenJDK-%{version}/bin/jdeprscan
%{_libdir}/jvm/OpenJDK-%{version}/bin/javac
%{_libdir}/jvm/OpenJDK-%{version}/bin/javadoc
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
%{_libdir}/jvm/OpenJDK-%{version}/bin/serialver
%{_libdir}/jvm/OpenJDK-%{version}/conf
%{_libdir}/jvm/OpenJDK-%{version}/jmods
%{_libdir}/jvm/OpenJDK-%{version}/bin/java
%{_libdir}/jvm/OpenJDK-%{version}/bin/jjs
%{_libdir}/jvm/OpenJDK-%{version}/bin/keytool
%{_libdir}/jvm/OpenJDK-%{version}/bin/pack200
%{_libdir}/jvm/OpenJDK-%{version}/bin/rmid
%{_libdir}/jvm/OpenJDK-%{version}/bin/rmiregistry
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
*   Thu Apr 25 2019 Tapas Kundu <tkundu@vmware.com> 1.11.0.2-2
-   Removed obsolete for openjdk
*   Tue Feb 12 2019 Tapas Kundu <tkundu@vmware.com> 1.11.0.2-1
-   Initial build. First version
