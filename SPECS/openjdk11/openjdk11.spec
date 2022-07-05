%define _use_internal_dependency_generator 0
%global security_hardening none
%define jdk_major_version 11.0
%define subversion 12
Summary:	OpenJDK
Name:		openjdk11
Version:	11.0.12
Release:	2%{?dist}
License:	GNU General Public License V2
URL:		https://openjdk.java.net
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:	http://www.java.net/download/openjdk/jdk/jdk11/openjdk-%{version}.tar.gz
%define sha512 openjdk-11.0=1bc7878ccb73e495907c02718573b63c88f61581340e8038ab4f0abf6161ac355d7a1a420de4949192b7df951cd39a1d890f251cba4647d8fd425c72d92d0164
BuildArch:      x86_64
BuildRequires:  pcre-devel
BuildRequires:	which
BuildRequires:	zip
BuildRequires:	unzip
BuildRequires:  zlib-devel
BuildRequires:	ca-certificates
BuildRequires:	chkconfig
BuildRequires:  freetype2
BuildRequires:  fontconfig-devel freetype2-devel glib-devel harfbuzz-devel elfutils-libelf-devel
Requires:       chkconfig
Obsoletes:      openjdk <= %{version}
AutoReqProv: 	no
%define ExtraBuildRequires icu-devel, cups, cups-devel, xorg-proto-devel, libXtst, libXtst-devel, libXfixes, libXfixes-devel, libXi, libXi-devel, openjdk, openjre, icu, alsa-lib, alsa-lib-devel, xcb-proto, libXdmcp-devel, libXau-devel, util-macros, xtrans, libxcb-devel, proto, libXdmcp, libxcb, libXau, xtrans-devel, libX11, libX11-devel, libXext, libXext-devel, libICE-devel, libSM, libICE, libSM-devel, libXt, libXmu, libXt-devel, libXmu-devel, libXrender, libXrender-devel, libXrandr, libXrandr-devel, openjre10, openjdk10
%define bootstrapjdkversion 1.8.0.112
%define jdk_major_version 1.11.0

%description
The OpenJDK package installs java class library and javac java compiler.

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
%autosetup -n openjdk-%{version}

%build
chmod a+x ./configur*
unset JAVA_HOME &&
ENABLE_HEADLESS_ONLY="true" &&
./configur* \
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
# make doesn't support _smp_mflags
make install

install -vdm755 %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}
chown -R root:root %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}
install -vdm755 %{buildroot}%{_bindir}
mv /usr/local/jvm/openjdk-%{version}-internal/* %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/
cp README LICENSE ASSEMBLY_EXCEPTION %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/

%post
alternatives --install %{_bindir}/javac javac %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javac 20000 \
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

alternatives --install %{_bindir}/java java %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/java 20000 \
  --slave %{_bindir}/jjs jjs %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jjs \
  --slave %{_bindir}/keytool keytool %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/keytool \
  --slave %{_bindir}/pack200 pack200 %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/pack200 \
  --slave %{_bindir}/rmid rmid %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/rmiregistry \
  --slave %{_bindir}/unpack200 unpack200 %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/unpack200
/sbin/ldconfig

%postun
# Do alternative remove only in case of uninstall
if [ $1 -eq 0 ]
then
  alternatives --remove javac %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javac
  alternatives --remove java %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/java
fi
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
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jaotc
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jar
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jhsdb
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jimage
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jarsigner
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jdeprscan
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javac
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javadoc
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
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/serialver
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/conf
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jmods
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/java
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jjs
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/keytool
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/pack200
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/rmid
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/rmiregistry
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/unpack200
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jfr
%exclude %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/*.debuginfo

%files doc
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/man/
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/legal/
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/demo

%files src
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/lib/src.zip

%changelog
*   Wed May 18 2022 Mukul Sikka <msikka@vmware.com> 11.0.12-2
-   Added alternative for java
*   Wed Mar 23 2022 Tapas Kundu <tkundu@vmware.com> 11.0.12-1
-   Update to tag jdk-11.0.12-ga
*   Wed Dec 15 2021 Tapas Kundu <tkundu@vmware.com> 11.0.9-2
-   Use openjdk10 from PublishXrpms
*   Wed Oct 21 2020 Tapas Kundu <tkundu@vmware.com> 11.0.9-1
-   Updated to 11.0.9 tag - jdk-11.0.9+10
*   Tue Aug 11 2020 Ankit Jain <ankitja@vmware.com> 11.0.8-2
-   Added a check in %postun to avoid alternatives --remove
-   after new version is installed.
-   Do alternative remove only in case of uninstall.
*   Fri Jul 24 2020 Shreyas B <shreyasb@vmware.com> 11.0.8-1
-   Updating to jdk-11.0.8-ga
*   Sun Apr 19 2020 Tapas Kundu <tkundu@vmware.com> 11.0.7-1
-   Updating to jdk-11.0.7-ga
*   Fri Oct 18 2019 Tapas Kundu <tkundu@vmware.com> 1.11.0.28-1
-   Updated to jdk11 tag: 11+28
*   Thu Apr 25 2019 Tapas Kundu <tkundu@vmware.com> 1.11.0.2-1
-   Initial build. First version
