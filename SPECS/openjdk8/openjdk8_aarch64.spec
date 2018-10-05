%define _use_internal_dependency_generator 0
%global security_hardening none
%define _jdk_update 151
%define _jdk_build 13
%define _repo_ver aarch64-jdk8u%{_jdk_update}-b%{_jdk_build}
%define _url_src http://hg.openjdk.java.net/aarch64-port/jdk8u

Summary:	OpenJDK
Name:		openjdk8
Version:	1.8.0.151
Release:	1%{?dist}
License:	GNU GPL
URL:		http://hg.openjdk.java.net/aarch64-port/jdk8u/
Group:		Development/Tools
Vendor:		VMware, Inc.
Distribution:   Photon
Source0:	%{_url_src}/archive/jdk8u-%{_repo_ver}.tar.bz2
%define sha1 jdk8u=d92f2f3633ca1f376dddc1d3c6d7ec53a54d7d63
Source1:	%{_url_src}/corba/archive/corba-%{_repo_ver}.tar.bz2
%define sha1 corba=a8cfcc8cd8817560059d7d121bb774334ae012b0
Source2:	%{_url_src}/hotspot/archive/hotspot-%{_repo_ver}.tar.bz2
%define sha1 hotspot=c9378ab34ee281e196206214ffe3174b2dfd2d80
Source3:	%{_url_src}/jdk/archive/jdk-%{_repo_ver}.tar.bz2
%define sha1 jdk-aarch64=5cc629011f0e6c2aa522e4ca6c8b602912431cbd
Source4:	%{_url_src}/jaxws/archive/jaxws-%{_repo_ver}.tar.bz2
%define sha1 jaxws=d3fd7bca75d6e8125c7968c9242129477d0fc0cb
Source5:	%{_url_src}/jaxp/archive/jaxp-%{_repo_ver}.tar.bz2
%define sha1 jaxp=229a83f8687bae8c1c51f2ea0010f3d2cf896072
Source6:	%{_url_src}/langtools/archive/langtools-%{_repo_ver}.tar.bz2
%define sha1 langtools=ec34f7adc4f66b687a33e1c8fbf0a4e44dafb0c1
Source7:	%{_url_src}/nashorn/archive/nashorn-%{_repo_ver}.tar.bz2
%define sha1 nashorn=aaf4d057bb3e5d8700f6b6d11d38fb9519c2ab29
Patch0:		Awt_build_headless_only.patch
Patch1:		check-system-ca-certs.patch
BuildRequires:  pcre-devel
BuildRequires:	which
BuildRequires:	zip
BuildRequires:	unzip
BuildRequires:  zlib-devel
BuildRequires:	ca-certificates
BuildRequires:	chkconfig
BuildRequires:  fontconfig-devel
BuildRequires:  freetype2-devel
BuildRequires:  glib-devel
BuildRequires:  harfbuzz-devel
Requires:       openjre8 = %{version}-%{release}
Requires:       chkconfig
Obsoletes:      openjdk <= %{version}
AutoReqProv: 	no
%define bootstrapjdk /usr/lib/jvm/OpenJDK-1.8.0.151
%description
The OpenJDK package installs java class library and javac java compiler.

%package	-n openjre8
Summary:	Java runtime environment
AutoReqProv: 	no
Obsoletes:      openjre <= %{version}
Requires:       chkconfig
Requires:	libstdc++
%description	-n openjre8
It contains the libraries files for Java runtime environment


%package	sample
Summary:	Sample java applications.
Group:          Development/Languages/Java
Obsoletes:      openjdk-sample <= %{version}
Requires:       %{name} = %{version}-%{release}
%description	sample
It contains the Sample java applications.

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
%setup -qn jdk8u-%{_repo_ver} -b1 -b2 -b3 -b4 -b5 -b6 -b7
for subrepo in corba hotspot jdk jaxws jaxp langtools nashorn
do
    mv ../${subrepo}-%{_repo_ver} ${subrepo}
done
%patch0 -p1
%patch1 -p1
rm jdk/src/solaris/native/sun/awt/CUPSfuncs.c
sed -i "s#\"ft2build.h\"#<ft2build.h>#g" jdk/src/share/native/sun/font/freetypeScaler.c
sed -i '0,/BUILD_LIBMLIB_SRC/s/BUILD_LIBMLIB_SRC/BUILD_HEADLESS_ONLY := 1\nOPENJDK_TARGET_OS := linux\n&/' jdk/make/lib/Awt2dLibraries.gmk

%build
chmod a+x ./configure
unset JAVA_HOME &&
./configure \
	CUPS_NOT_NEEDED=yes \
	--with-target-bits=64 \
	--with-boot-jdk=%{bootstrapjdk} \
	--disable-headful \
	--with-cacerts-file=%{bootstrapjdk}/jre/lib/security/cacerts \
	--with-extra-cxxflags="-Wno-error -std=gnu++98 -fno-delete-null-pointer-checks -fno-lifetime-dse" \
	--with-extra-cflags="-std=gnu++98 -fno-delete-null-pointer-checks -Wno-error -fno-lifetime-dse" \
	--with-freetype-include=/usr/include/freetype2 \
	--with-freetype-lib=/usr/lib \
	--with-stdc++lib=dynamic

make \
    DEBUG_BINARIES=true \
    BUILD_HEADLESS_ONLY=1 \
    OPENJDK_TARGET_OS=linux \
    JAVAC_FLAGS=-g \
    STRIP_POLICY=no_strip \
    DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
    CLASSPATH=%{bootstrapjdk}/jre \
    POST_STRIP_CMD="" \
    LOG=trace \
    SCTP_WERROR=

%install
make DESTDIR=%{buildroot} install \
	BUILD_HEADLESS_ONLY=yes \
	OPENJDK_TARGET_OS=linux \
	DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
	CLASSPATH=%{bootstrapjdk}/jre

install -vdm755 %{buildroot}%{_libdir}/jvm/OpenJDK-%{version}
chown -R root:root %{buildroot}%{_libdir}/jvm/OpenJDK-%{version}
install -vdm755 %{buildroot}%{_bindir}
find /usr/local/jvm/openjdk-1.8.0-internal/jre/lib/aarch64 -iname \*.diz -delete
mv /usr/local/jvm/openjdk-1.8.0-internal/* %{buildroot}%{_libdir}/jvm/OpenJDK-%{version}/

%post
alternatives --install %{_bindir}/javac javac %{_libdir}/jvm/OpenJDK-%{version}/bin/javac 2000 \
  --slave %{_bindir}/appletviewer appletviewer %{_libdir}/jvm/OpenJDK-%{version}/bin/appletviewer \
  --slave %{_bindir}/extcheck extcheck %{_libdir}/jvm/OpenJDK-%{version}/bin/extcheck \
  --slave %{_bindir}/idlj idlj %{_libdir}/jvm/OpenJDK-%{version}/bin/idlj \
  --slave %{_bindir}/jar jar %{_libdir}/jvm/OpenJDK-%{version}/bin/jar \
  --slave %{_bindir}/jarsigner jarsigner %{_libdir}/jvm/OpenJDK-%{version}/bin/jarsigner \
  --slave %{_bindir}/javadoc javadoc %{_libdir}/jvm/OpenJDK-%{version}/bin/javadoc \
  --slave %{_bindir}/javah javah %{_libdir}/jvm/OpenJDK-%{version}/bin/javah \
  --slave %{_bindir}/javap javap %{_libdir}/jvm/OpenJDK-%{version}/bin/javap \
  --slave %{_bindir}/jcmd jcmd %{_libdir}/jvm/OpenJDK-%{version}/bin/jcmd \
  --slave %{_bindir}/jconsole jconsole %{_libdir}/jvm/OpenJDK-%{version}/bin/jconsole \
  --slave %{_bindir}/jdb jdb %{_libdir}/jvm/OpenJDK-%{version}/bin/jdb \
  --slave %{_bindir}/jdeps jdeps %{_libdir}/jvm/OpenJDK-%{version}/bin/jdeps \
  --slave %{_bindir}/jhat jhat %{_libdir}/jvm/OpenJDK-%{version}/bin/jhat \
  --slave %{_bindir}/jinfo jinfo %{_libdir}/jvm/OpenJDK-%{version}/bin/jinfo \
  --slave %{_bindir}/jmap jmap %{_libdir}/jvm/OpenJDK-%{version}/bin/jmap \
  --slave %{_bindir}/jps jps %{_libdir}/jvm/OpenJDK-%{version}/bin/jps \
  --slave %{_bindir}/jrunscript jrunscript %{_libdir}/jvm/OpenJDK-%{version}/bin/jrunscript \
  --slave %{_bindir}/jsadebugd jsadebugd %{_libdir}/jvm/OpenJDK-%{version}/bin/jsadebugd \
  --slave %{_bindir}/jstack jstack %{_libdir}/jvm/OpenJDK-%{version}/bin/jstack \
  --slave %{_bindir}/jstat jstat %{_libdir}/jvm/OpenJDK-%{version}/bin/jstat \
  --slave %{_bindir}/jstatd jstatd %{_libdir}/jvm/OpenJDK-%{version}/bin/jstatd \
  --slave %{_bindir}/native2ascii native2ascii %{_libdir}/jvm/OpenJDK-%{version}/bin/native2ascii \
  --slave %{_bindir}/rmic rmic %{_libdir}/jvm/OpenJDK-%{version}/bin/rmic \
  --slave %{_bindir}/schemagen schemagen %{_libdir}/jvm/OpenJDK-%{version}/bin/schemagen \
  --slave %{_bindir}/serialver serialver %{_libdir}/jvm/OpenJDK-%{version}/bin/serialver \
  --slave %{_bindir}/wsgen wsgen %{_libdir}/jvm/OpenJDK-%{version}/bin/wsgen \
  --slave %{_bindir}/wsimport wsimport %{_libdir}/jvm/OpenJDK-%{version}/bin/wsimport \
  --slave %{_bindir}/xjc xjc %{_libdir}/jvm/OpenJDK-%{version}/bin/xjc
/sbin/ldconfig

%post -n openjre8
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

%postun -n openjre8
alternatives --remove java %{_libdir}/jvm/OpenJDK-%{version}/jre/bin/java
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{version}/ASSEMBLY_EXCEPTION
%{_libdir}/jvm/OpenJDK-%{version}/LICENSE
%{_libdir}/jvm/OpenJDK-%{version}/release
%{_libdir}/jvm/OpenJDK-%{version}/THIRD_PARTY_README
%{_libdir}/jvm/OpenJDK-%{version}/lib
%{_libdir}/jvm/OpenJDK-%{version}/include/
%{_libdir}/jvm/OpenJDK-%{version}/bin/extcheck
%{_libdir}/jvm/OpenJDK-%{version}/bin/idlj
%{_libdir}/jvm/OpenJDK-%{version}/bin/jar
%{_libdir}/jvm/OpenJDK-%{version}/bin/jarsigner
%{_libdir}/jvm/OpenJDK-%{version}/bin/java-rmi.cgi
%{_libdir}/jvm/OpenJDK-%{version}/bin/javac
%{_libdir}/jvm/OpenJDK-%{version}/bin/javadoc
%{_libdir}/jvm/OpenJDK-%{version}/bin/javah
%{_libdir}/jvm/OpenJDK-%{version}/bin/javap
%{_libdir}/jvm/OpenJDK-%{version}/bin/jcmd
%{_libdir}/jvm/OpenJDK-%{version}/bin/jconsole
%{_libdir}/jvm/OpenJDK-%{version}/bin/jdb
%{_libdir}/jvm/OpenJDK-%{version}/bin/jdeps
%{_libdir}/jvm/OpenJDK-%{version}/bin/jhat
%{_libdir}/jvm/OpenJDK-%{version}/bin/jinfo
%{_libdir}/jvm/OpenJDK-%{version}/bin/jjs
%{_libdir}/jvm/OpenJDK-%{version}/bin/jmap
%{_libdir}/jvm/OpenJDK-%{version}/bin/jps
%{_libdir}/jvm/OpenJDK-%{version}/bin/jrunscript
%{_libdir}/jvm/OpenJDK-%{version}/bin/jsadebugd
%{_libdir}/jvm/OpenJDK-%{version}/bin/jstack
%{_libdir}/jvm/OpenJDK-%{version}/bin/jstat
%{_libdir}/jvm/OpenJDK-%{version}/bin/jstatd
%{_libdir}/jvm/OpenJDK-%{version}/bin/native2ascii
%{_libdir}/jvm/OpenJDK-%{version}/bin/rmic
%{_libdir}/jvm/OpenJDK-%{version}/bin/schemagen
%{_libdir}/jvm/OpenJDK-%{version}/bin/serialver
%{_libdir}/jvm/OpenJDK-%{version}/bin/wsgen
%{_libdir}/jvm/OpenJDK-%{version}/bin/wsimport
%{_libdir}/jvm/OpenJDK-%{version}/bin/xjc

%files	-n openjre8
%defattr(-,root,root)
%dir %{_libdir}/jvm/OpenJDK-%{version}
%{_libdir}/jvm/OpenJDK-%{version}/jre/
%{_libdir}/jvm/OpenJDK-%{version}/bin/java
%{_libdir}/jvm/OpenJDK-%{version}/bin/keytool
%{_libdir}/jvm/OpenJDK-%{version}/bin/orbd
%{_libdir}/jvm/OpenJDK-%{version}/bin/pack200
%{_libdir}/jvm/OpenJDK-%{version}/bin/rmid
%{_libdir}/jvm/OpenJDK-%{version}/bin/rmiregistry
%{_libdir}/jvm/OpenJDK-%{version}/bin/servertool
%{_libdir}/jvm/OpenJDK-%{version}/bin/tnameserv
%{_libdir}/jvm/OpenJDK-%{version}/bin/unpack200
%{_libdir}/jvm/OpenJDK-%{version}/lib/aarch64/jli/
%exclude %{_libdir}/jvm/OpenJDK-%{version}/lib/aarch64/*.diz

%files sample
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{version}/sample/

%files doc
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{version}/man/
%{_libdir}/jvm/OpenJDK-%{version}/demo

%files src
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{version}/src.zip

%changelog
*   Thu Dec 21 2017 Alexey Makhalov <amakhalov@vmware.com> 1.8.0.151-1
-   Initial version of OpenJDK for aarch64. SPEC file was forked from
    openjdk8-1.8.0.152-1 of x86_64
