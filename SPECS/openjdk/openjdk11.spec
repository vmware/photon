%define bootstrap           0
%global security_hardening  none
%define jdk_major_version   1.11.0
%define _jobs %(echo $(( ($(nproc)+1) / 2 )))
%define jdkInstallDir %{_libdir}/jvm/OpenJDK-%{jdk_major_version}

%if 0%{?bootstrap} == 1
%ifarch aarch64
%define bootstrapTarName 11.0.28_6
%define bootstrapDirName jdk-11.0.28+6
%endif

%ifarch x86_64
%define bootstrapTarName 11.0.2
%define bootstrapDirName jdk-%{bootstrapTarName}
%endif
%endif

Summary:        OpenJDK
Name:           openjdk11
Version:        11.0.30
Release:        3%{?dist}
URL:            https://github.com/openjdk/jdk11u
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://github.com/openjdk/jdk11u/archive/refs/tags/jdk-%{version}-ga.tar.gz

%if 0%{?bootstrap} == 1
%ifarch x86_64
Source1: https://download.java.net/java/GA/jdk11/9/GPL/openjdk-%{bootstrapTarName}_linux-x64_bin.tar.gz
%endif

%ifarch aarch64
Source1: https://github.com/adoptium/temurin11-binaries/releases/download/%{bootstrapTarName}/OpenJDK11U-jdk_aarch64_linux_hotspot_%{bootstrapTarName}.tar.gz
%endif
%endif

Source2: license-openjdk11.txt
%include %{SOURCE2}

BuildRequires: pcre-devel
BuildRequires: which
BuildRequires: zip
BuildRequires: unzip
BuildRequires: zlib-devel
BuildRequires: ca-certificates
BuildRequires: fontconfig-devel
BuildRequires: freetype2-devel
BuildRequires: glib-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: alsa-lib-devel
BuildRequires: libXrender-devel
BuildRequires: libxcb-devel
BuildRequires: libXrandr-devel
BuildRequires: libXtst-devel
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: cups-devel

%if 0%{?bootstrap} == 0
%define ExtraBuildRequires openjdk11
%endif

Requires: alternatives
Requires(postun): alternatives

Requires: %{name}-jre = %{version}-%{release}

Obsoletes: openjdk <= %{version}

AutoReqProv: no

%description
The OpenJDK package installs java class library and javac java compiler.

%package        jre
Summary:        JRE subset files from jdk11
Requires:       alternatives
Requires(postun): alternatives
Requires:       alsa-lib
Requires:       freetype2
Requires:       libstdc++
Requires:       libgcc
Requires:       zlib

Conflicts: %{name} < 11.0.20-4%{?dist}
Provides: libjli.so()(64bit)
Provides: jre = %{version}

%description    jre
%{summary}

%package        doc
Summary:        Documentation and demo applications for openjdk
Group:          Development/Languages/Java
Obsoletes:      openjdk-doc <= %{version}
Requires:       %{name} = %{version}-%{release}

%description    doc
It contains the documentation and demo applications for openjdk

%package        src
Summary:        OpenJDK Java classes for developers
Group:          Development/Languages/Java
Obsoletes:      openjdk-src <= %{version}
Requires:       %{name} = %{version}-%{release}

%description    src
This package provides the runtime library class sources.

%prep
%autosetup -p1 -n jdk11u-jdk-%{version}-ga
%if 0%{?bootstrap} == 1
tar xf %{SOURCE1} -C %{_var}/opt
%endif

# avoid libpng-6.x license
rm -r src/java.desktop/macosx \
      src/java.desktop/share/native/libsplashscreen \
      src/java.desktop/share/legal/libpng.md

%build
unset JAVA_HOME
ENABLE_HEADLESS_ONLY="true"

sh ./configure \
%if 0%{?bootstrap} == 1
    --with-boot-jdk=%{_var}/opt/%{bootstrapDirName} \
%endif
    --with-target-bits=64 \
    --enable-headless-only \
    --with-extra-cxxflags="-Wno-error -std=gnu++98 -fno-delete-null-pointer-checks -fno-lifetime-dse" \
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

install -vdm755 %{buildroot}%{jdkInstallDir}
chown -R root:root %{buildroot}%{jdkInstallDir}
install -vdm755 %{buildroot}%{_bindir}

mv %{_usr}/local/jvm/openjdk-%{version}-internal/* \
        %{buildroot}%{jdkInstallDir}/

cp README.md LICENSE ASSEMBLY_EXCEPTION \
        %{buildroot}%{jdkInstallDir}/

%post jre
alternatives --install %{_bindir}/java java %{jdkInstallDir}/bin/java 20000 \
  --slave %{_bindir}/jjs jjs %{jdkInstallDir}/bin/jjs \
  --slave %{_bindir}/keytool keytool %{jdkInstallDir}/bin/keytool \
  --slave %{_bindir}/pack200 pack200 %{jdkInstallDir}/bin/pack200 \
  --slave %{_bindir}/rmid rmid %{jdkInstallDir}/bin/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{jdkInstallDir}/bin/rmiregistry \
  --slave %{_bindir}/unpack200 unpack200 %{jdkInstallDir}/bin/unpack200

%postun jre
if [ $1 -eq 0 ]; then
  alternatives --remove java %{jdkInstallDir}/bin/java
fi

%post
alternatives --install %{_bindir}/javac javac %{jdkInstallDir}/bin/javac 20000 \
  --slave %{_bindir}/appletviewer appletviewer %{jdkInstallDir}/bin/appletviewer \
  --slave %{_bindir}/idlj idlj %{jdkInstallDir}/bin/idlj \
  --slave %{_bindir}/jaotc jaotc %{jdkInstallDir}/bin/jaotc \
  --slave %{_bindir}/jar jar %{jdkInstallDir}/bin/jar \
  --slave %{_bindir}/jarsigner jarsigner %{jdkInstallDir}/bin/jarsigner \
  --slave %{_bindir}/jhsdb jhsdb %{jdkInstallDir}/bin/jhsdb \
  --slave %{_bindir}/jimage jimage %{jdkInstallDir}/bin/jimage \
  --slave %{_bindir}/jlink jlink %{jdkInstallDir}/bin/jlink \
  --slave %{_bindir}/jmod jmod %{jdkInstallDir}/bin/jmod \
  --slave %{_bindir}/javadoc javadoc %{jdkInstallDir}/bin/javadoc \
  --slave %{_bindir}/javah javah %{jdkInstallDir}/bin/javah \
  --slave %{_bindir}/javap javap %{jdkInstallDir}/bin/javap \
  --slave %{_bindir}/jcmd jcmd %{jdkInstallDir}/bin/jcmd \
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
  --slave %{_bindir}/rmic rmic %{jdkInstallDir}/bin/rmic \
  --slave %{_bindir}/schemagen schemagen %{jdkInstallDir}/bin/schemagen \
  --slave %{_bindir}/serialver serialver %{jdkInstallDir}/bin/serialver \
  --slave %{_bindir}/wsgen wsgen %{jdkInstallDir}/bin/wsgen \
  --slave %{_bindir}/wsimport wsimport %{jdkInstallDir}/bin/wsimport \
  --slave %{_bindir}/xjc xjc %{jdkInstallDir}/bin/xjc

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
%{jdkInstallDir}/bin/jaotc
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
%{jdkInstallDir}/bin/rmic
%{jdkInstallDir}/bin/serialver
%{jdkInstallDir}/bin/jhsdb
%{jdkInstallDir}/bin/jimage
%{jdkInstallDir}/bin/jdeprscan
%{jdkInstallDir}/bin/jfr
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
%{jdkInstallDir}/bin/jjs
%{jdkInstallDir}/bin/keytool
%{jdkInstallDir}/bin/pack200
%{jdkInstallDir}/bin/rmid
%{jdkInstallDir}/bin/rmiregistry
%{jdkInstallDir}/bin/unpack200
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
* Thu Mar 12 2026 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 11.0.30-3
- Require alternatives instead of chkconfig
* Sun Feb 15 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 11.0.30-2
- Use _use_internal_dependency_generator, latest rpm doesn't allow disabling it
* Tue Feb 10 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 11.0.30-1
- Upgrade to v11.0.30
* Wed Nov 12 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 11.0.29-2
- Bootstrap using upstream jdk binaries
* Mon Nov 10 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 11.0.29-1
- Version upgrade to address CVEs
* Fri Aug 22 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 11.0.28-1
- Upgrade to v11.0.28
* Wed Jan 22 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 11.0.26-1
- Upgrade to v11.0.26
* Mon Dec 16 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 11.0.20-9
- Version bump as a part of cups upgrade
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 11.0.20-8
- Release bump for SRP compliance
* Tue Sep 10 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 11.0.20-7
- Cleanup Extra BuildRequires
* Fri Sep 29 2023 Srish Srinivasan <ssrish@vmware.com> 11.0.20-6
- Version bump as a part of cups upgrade
* Mon Sep 04 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 11.0.20-5
- Add provides java for jre subpackage
* Mon Aug 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 11.0.20-4
- Add jre subpackage
- Change alternatives accordingly
* Mon Jul 10 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 11.0.20-3
- Bump version as a part of cups upgrade
* Tue Jun 27 2023 Kuntal Nayak <nkuntal@vmware.com> 11.0.20-2
- Version upgrade for CVE-2016-7945 fix
* Fri Jun 16 2023 Shreenidhi Shedi <sshedi@vmware.com> 11.0.20-1
- Upgrade to v11.0.20
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 11.0.18-3
- Bump version as a part of freetype2 upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 11.0.18-2
- Bump version as a part of zlib upgrade
* Tue Feb 14 2023 Mukul Sikka <msikka@vmware.com> 11.0.18-1
- Updating to jdk-11.0.18-ga
* Sat Feb 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 11.0.12-6
- Bump version as a part of icu upgrade
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 11.0.12-5
- Bump up due to change in elfutils
* Thu Oct 06 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 11.0.12-4
- Rebuild with latest toolchain
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 11.0.12-3
- Bump version as a part of icu upgrade
* Wed May 18 2022 Mukul Sikka <msikka@vmware.com> 11.0.12-2
- Added alternative for java
* Wed Mar 23 2022 Tapas Kundu <tkundu@vmware.com> 11.0.12-1
- Update to tag jdk-11.0.12-ga
* Wed Dec 15 2021 Tapas Kundu <tkundu@vmware.com> 11.0.9-2
- Use openjdk10 from PublishXrpms
* Wed Oct 21 2020 Tapas Kundu <tkundu@vmware.com> 11.0.9-1
- Updated to 11.0.9 tag - jdk-11.0.9+10
* Tue Aug 11 2020 Ankit Jain <ankitja@vmware.com> 11.0.8-2
- Added a check in %postun to avoid alternatives --remove
- after new version is installed.
- Do alternative remove only in case of uninstall.
* Fri Jul 24 2020 Shreyas B <shreyasb@vmware.com> 11.0.8-1
- Updating to jdk-11.0.8-ga
* Sun Apr 19 2020 Tapas Kundu <tkundu@vmware.com> 11.0.7-1
- Updating to jdk-11.0.7-ga
* Fri Oct 18 2019 Tapas Kundu <tkundu@vmware.com> 1.11.0.28-1
- Updated to jdk11 tag: 11+28
* Thu Apr 25 2019 Tapas Kundu <tkundu@vmware.com> 1.11.0.2-1
- Initial build. First version
