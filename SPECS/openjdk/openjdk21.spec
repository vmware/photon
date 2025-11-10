%global security_hardening  none
%define jdk_major_version   21
%define _use_internal_dependency_generator 0
%define _jobs %(echo $(( ($(nproc)+1) / 2 )))
%define jdkInstallDir %{_libdir}/jvm/OpenJDK-%{jdk_major_version}

Summary:    OpenJDK
Name:       openjdk21
Version:    21.0.9
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
make images JOBS=%{_jobs}

install -vdm755 %{buildroot}%{jdkInstallDir}
chown -R root:root %{buildroot}%{jdkInstallDir}
install -vdm755 %{buildroot}%{_bindir}

mv build/linux-%{_arch}-server-release/images/jdk/* \
    %{buildroot}%{jdkInstallDir}/

cp README.md LICENSE ASSEMBLY_EXCEPTION \
        %{buildroot}%{jdkInstallDir}/

%post jre
alternatives --install %{_bindir}/java java %{jdkInstallDir}/bin/java 40000 \
  --slave %{_bindir}/keytool keytool %{jdkInstallDir}/bin/keytool \
  --slave %{_bindir}/rmiregistry rmiregistry %{jdkInstallDir}/bin/rmiregistry

%postun jre
if [ $1 -eq 0 ]; then
  alternatives --remove java %{jdkInstallDir}/bin/java
fi

%post
alternatives --install %{_bindir}/javac javac %{jdkInstallDir}/bin/javac 40000 \
  --slave %{_bindir}/jar jar %{jdkInstallDir}/bin/jar \
  --slave %{_bindir}/jarsigner jarsigner %{jdkInstallDir}/bin/jarsigner \
  --slave %{_bindir}/jhsdb jhsdb %{jdkInstallDir}/bin/jhsdb \
  --slave %{_bindir}/jimage jimage %{jdkInstallDir}/bin/jimage \
  --slave %{_bindir}/jlink jlink %{jdkInstallDir}/bin/jlink \
  --slave %{_bindir}/jmod jmod %{jdkInstallDir}/bin/jmod \
  --slave %{_bindir}/javadoc javadoc %{jdkInstallDir}/bin/javadoc \
  --slave %{_bindir}/jdeprscan jdeprscan %{jdkInstallDir}/bin/jdeprscan \
  --slave %{_bindir}/jconsole jconsole %{jdkInstallDir}/bin/jconsole \
  --slave %{_bindir}/jdb jdb %{jdkInstallDir}/bin/jdb \
  --slave %{_bindir}/jdeps jdeps %{jdkInstallDir}/bin/jdeps \
  --slave %{_bindir}/jinfo jinfo %{jdkInstallDir}/bin/jinfo \
  --slave %{_bindir}/jmap jmap %{jdkInstallDir}/bin/jmap \
  --slave %{_bindir}/jps jps %{jdkInstallDir}/bin/jps \
  --slave %{_bindir}/jrunscript jrunscript %{jdkInstallDir}/bin/jrunscript \
  --slave %{_bindir}/jstack jstack %{jdkInstallDir}/bin/jstack \
  --slave %{_bindir}/jstat jstat %{jdkInstallDir}/bin/jstat \
  --slave %{_bindir}/jstatd jstatd %{jdkInstallDir}/bin/jstatd \
  --slave %{_bindir}/serialver serialver %{jdkInstallDir}/bin/serialver \
  --slave %{_bindir}/jpackage jpackage %{jdkInstallDir}/bin/jpackage \
  --slave %{_bindir}/javap javap %{jdkInstallDir}/bin/javap \
  --slave %{_bindir}/jcmd jcmd %{jdkInstallDir}/bin/jcmd \
  --slave %{_bindir}/jshell jshell %{jdkInstallDir}/bin/jshell \
  --slave %{_bindir}/jfr jfr %{jdkInstallDir}/bin/jfr \
  --slave %{_bindir}/jwebserver jwebserver %{jdkInstallDir}/bin/jwebserver

%postun
# Do alternative remove only in case of uninstall
if [ $1 -eq 0 ]; then
  alternatives --remove javac %{jdkInstallDir}/bin/javac
fi

%clean
rm -rf %{buildroot}/* %{_libdir}/jvm/OpenJDK-*

%files
%defattr(-,root,root)
%{jdkInstallDir}/LICENSE
%{jdkInstallDir}/README.md
%{jdkInstallDir}/bin/jar
%{jdkInstallDir}/bin/jarsigner
%{jdkInstallDir}/bin/javac
%{jdkInstallDir}/bin/javadoc
%{jdkInstallDir}/bin/javap
%{jdkInstallDir}/bin/jcmd
%{jdkInstallDir}/bin/jconsole
%{jdkInstallDir}/bin/jdb
%{jdkInstallDir}/bin/jdeps
%{jdkInstallDir}/bin/jinfo
%{jdkInstallDir}/bin/jlink
%{jdkInstallDir}/bin/jmod
%{jdkInstallDir}/bin/jmap
%{jdkInstallDir}/bin/jps
%{jdkInstallDir}/bin/jshell
%{jdkInstallDir}/bin/jrunscript
%{jdkInstallDir}/bin/jstack
%{jdkInstallDir}/bin/jstat
%{jdkInstallDir}/bin/jstatd
%{jdkInstallDir}/bin/serialver
%{jdkInstallDir}/bin/jhsdb
%{jdkInstallDir}/bin/jimage
%{jdkInstallDir}/bin/jdeprscan
%{jdkInstallDir}/bin/jfr
%{jdkInstallDir}/bin/jpackage
%{jdkInstallDir}/bin/jwebserver
%{jdkInstallDir}/include/
%{jdkInstallDir}/lib/ct.sym

%files jre
%defattr(-,root,root)
%{jdkInstallDir}/ASSEMBLY_EXCEPTION
%{jdkInstallDir}/release
%{jdkInstallDir}/lib
%exclude %{jdkInstallDir}/lib/ct.sym
%{jdkInstallDir}/conf
%{jdkInstallDir}/jmods
%{jdkInstallDir}/bin/java
%{jdkInstallDir}/bin/keytool
%{jdkInstallDir}/bin/rmiregistry
%exclude %{jdkInstallDir}/bin/*.debuginfo

%files doc
%defattr(-,root,root)
%{jdkInstallDir}/man/
%{jdkInstallDir}/legal/
%{jdkInstallDir}/demo

%files src
%defattr(-,root,root)
%{jdkInstallDir}/lib/src.zip

%changelog
* Mon Nov 10 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 21.0.9-1
- Version upgrade to address CVEs
* Fri Aug 22 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 21.0.8-1
- Upgrade to v21.0.8
* Wed Jan 22 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 21.0.6-1
- Upgrade to v21.0.6
* Sun Dec 15 2024 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 21.0.5-1
- Initial build. First version of openjdk21.
