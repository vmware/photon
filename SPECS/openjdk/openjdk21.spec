%global security_hardening  none
%define jdk_major_version   21
%define _use_internal_dependency_generator 0
%define _jobs %(echo $(( ($(nproc)+1) / 2 )))

Summary:    OpenJDK
Name:       openjdk21
Version:    21.0.6
Release:    1%{?dist}
URL:        https://github.com/openjdk/jdk21u
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/openjdk/jdk21u/archive/refs/tags/jdk-%{version}-ga.tar.gz

Source1: license-openjdk21.txt
%include %{SOURCE1}

BuildRequires: pcre-devel
BuildRequires: which
BuildRequires: zip
BuildRequires: unzip
BuildRequires: zlib-devel
BuildRequires: ca-certificates
BuildRequires: chkconfig
BuildRequires: freetype2
BuildRequires: fontconfig-devel
BuildRequires: freetype2-devel
BuildRequires: glib-devel
BuildRequires: harfbuzz-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: icu icu-devel
BuildRequires: cups cups-devel
BuildRequires: libXtst libXtst-devel libXi libXi-devel
BuildRequires: alsa-lib alsa-lib-devel util-macros
BuildRequires: xcb-proto libXdmcp libXdmcp-devel libXau-devel
BuildRequires: xtrans libxcb-devel proto libxcb libXau
BuildRequires: libX11 libX11-devel libXext libXext-devel
BuildRequires: libXt libXt-devel libXrender libXrender-devel
BuildRequires: libXrandr libXrandr-devel

Requires: chkconfig
Requires(postun): chkconfig

Requires: %{name}-jre = %{version}-%{release}

AutoReqProv: no

%define ExtraBuildRequires openjdk21, openjdk21-jre

%description
OpenJDK package installs javac and JDK tools.

%package        jre
Summary:        JRE subset files from jdk21
Requires:       chkconfig
Requires(postun): chkconfig
Requires:       alsa-lib
Requires:       freetype2
Requires:       libstdc++
Requires:       libgcc
Requires:       zlib

Provides:       libjli.so()(64bit)
Provides:       jre = %{version}

%description    jre
OpenJDK shared libraries and Java runtime modules.

%package        doc
Summary:        Documentation and demo applications for openjdk
Group:          Development/Languages/Java
Requires:       %{name} = %{version}-%{release}

%description    doc
Documentation and demo applications for OpenJDK.

%package        src
Summary:        OpenJDK Java classes for developers
Group:          Development/Languages/Java
Requires:       %{name} = %{version}-%{release}

%description    src
This package provides the runtime library class sources.

%prep
%autosetup -p1 -n jdk21u-jdk-%{version}-ga

%build
chmod a+x ./configur*
unset JAVA_HOME
ENABLE_HEADLESS_ONLY="true"

sh ./configur* \
    --with-target-bits=64 \
    --enable-headless-only \
    --with-extra-cxxflags="-Wno-error -fno-delete-null-pointer-checks -fno-lifetime-dse" \
    --with-extra-cflags="-fno-delete-null-pointer-checks -Wno-error -fno-lifetime-dse" \
    --with-freetype-include=%{_includedir}/freetype2 \
    --with-freetype-lib=%{_libdir} \
    --with-stdc++lib=dynamic \
    --disable-warnings-as-errors

mkdir -p %{_datadir}/java
# make doesn't support _smp_mflags
make \
    DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
    SCTP_WERROR= \
    BUILD_HEADLESS_ONLY=1 \
    OPENJDK_TARGET_OS=linux \
    STRIP_POLICY=no_strip \
    POST_STRIP_CMD="" \
    LOG=trace \
    JOBS=%{_jobs}

%install
unset JAVA_HOME
# make doesn't support _smp_mflags
make install JOBS=%{_jobs}

install -vdm755 %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}
chown -R root:root %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}
install -vdm755 %{buildroot}%{_bindir}

mv %{_usr}/local/jvm/openjdk-%{version}-internal/* \
        %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/

cp README.md LICENSE ASSEMBLY_EXCEPTION \
        %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/

%post jre
alternatives --install %{_bindir}/java java %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/java 40000 \
  --slave %{_bindir}/keytool keytool %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/keytool \
  --slave %{_bindir}/rmiregistry rmiregistry %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/rmiregistry

%postun jre
if [ $1 -eq 0 ]; then
  alternatives --remove java %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/java
fi

%post
alternatives --install %{_bindir}/javac javac %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javac 40000 \
  --slave %{_bindir}/jar jar %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jar \
  --slave %{_bindir}/jarsigner jarsigner %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jarsigner \
  --slave %{_bindir}/jhsdb jhsdb %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jhsdb \
  --slave %{_bindir}/jimage jimage %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jimage \
  --slave %{_bindir}/jlink jlink %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jlink \
  --slave %{_bindir}/jmod jmod %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jmod \
  --slave %{_bindir}/javadoc javadoc %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javadoc \
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
  --slave %{_bindir}/serialver serialver %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/serialver \
  --slave %{_bindir}/jpackage jpackage %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jpackage \
  --slave %{_bindir}/javap javap %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javap \
  --slave %{_bindir}/jcmd jcmd %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jcmd \
  --slave %{_bindir}/jshell jshell %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jshell \
  --slave %{_bindir}/jfr jfr %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jfr \
  --slave %{_bindir}/jwebserver jwebserver %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jwebserver

%postun
# Do alternative remove only in case of uninstall
if [ $1 -eq 0 ]; then
  alternatives --remove javac %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javac
fi

%clean
rm -rf %{buildroot}/* %{_libdir}/jvm/OpenJDK-*

%files
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/LICENSE
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/README.md
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jar
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jarsigner
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
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/serialver
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jhsdb
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jimage
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jdeprscan
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jfr
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jpackage
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jwebserver
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/include/
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/lib/ct.sym

%files jre
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/ASSEMBLY_EXCEPTION
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/release
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/lib
%exclude %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/lib/ct.sym
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/conf
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jmods
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/java
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/keytool
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/rmiregistry
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
* Wed Jan 22 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 21.0.6-1
- Upgrade to v21.0.6
* Sun Dec 15 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 21.0.5-1
- Initial build. First version of openjdk21.
