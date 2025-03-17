%global security_hardening  none
%define jdk_major_version   17
%define _use_internal_dependency_generator 0
%define _jobs %(echo $(( ($(nproc)+1) / 2 )))

Summary:    OpenJDK
Name:       openjdk17
Version:    17.0.14
Release:    1%{?dist}
URL:        https://github.com/openjdk/jdk17u
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/openjdk/jdk17u/archive/refs/tags/jdk-%{version}-ga.tar.gz

Source1: license-openjdk17.txt
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

Obsoletes: openjdk <= %{version}

AutoReqProv: no

%define ExtraBuildRequires openjdk17

%description
The OpenJDK package installs java class library and javac java compiler.

%package        jre
Summary:        JRE subset files from jdk11
Requires:       chkconfig
Requires(postun): chkconfig
Requires:       alsa-lib
Requires:       freetype2
Requires:       libstdc++
Requires:       libgcc
Requires:       zlib

Conflicts:      %{name} < 17.0.8-4%{?dist}

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

Provides:       jre = %{version}

%description    src
This package provides the runtime library class sources.

%prep
%autosetup -p1 -n jdk17u-jdk-%{version}-ga

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
alternatives --install %{_bindir}/java java %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/java 30000 \
  --slave %{_bindir}/keytool keytool %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/keytool \
  --slave %{_bindir}/pack200 pack200 %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/pack200 \
  --slave %{_bindir}/rmiregistry rmiregistry %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/rmiregistry

%postun jre
if [ $1 -eq 0 ]; then
  alternatives --remove java %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/java
fi

%post
alternatives --install %{_bindir}/javac javac %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javac 30000 \
  --slave %{_bindir}/appletviewer appletviewer %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/appletviewer \
  --slave %{_bindir}/idlj idlj %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/idlj \
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
  --slave %{_bindir}/schemagen schemagen %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/schemagen \
  --slave %{_bindir}/serialver serialver %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/serialver \
  --slave %{_bindir}/wsgen wsgen %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/wsgen \
  --slave %{_bindir}/wsimport wsimport %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/wsimport \
  --slave %{_bindir}/xjc xjc %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/xjc \
  --slave %{_bindir}/jpackage jpackage %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jpackage

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
* Wed Jan 22 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 17.0.14-1
- Upgrade to v17.0.14
* Mon Dec 16 2024 Brennan Lamoreaux <brennan.lamoreaux@broadcom.com> 17.0.13-3
- Version bump as a part of cups upgrade
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 17.0.13-2
- Release bump for SRP compliance
* Tue Oct 29 2024 Tapas Kundu <tapas.kundu@broadcom.com> 17.0.13-1
- Update to version 17.0.13
* Tue Sep 10 2024 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 17.0.8-7
- Cleanup Extra BuildRequires
* Fri Sep 29 2023 Srish Srinivasan <ssrish@vmware.com> 17.0.8-6
- Version bump as a part of cups upgrade
* Mon Sep 04 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 17.0.8-5
- Add provides java for jre subpackage
* Mon Aug 21 2023 Shreenidhi Shedi <sshedi@vmware.com> 17.0.8-4
- Add jre subpackage
- Change alternatives accordingly
* Mon Jul 10 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 17.0.8-3
- Bump version as a part of cups upgrade
* Tue Jun 27 2023 Kuntal Nayak <nkuntal@vmware.com> 17.0.8-2
- Version upgrade for CVE-2016-7945 fix
* Wed Jun 14 2023 Shivani Agarwal <shivania2@vmware.com> 17.0.8-1
- Update to jdk-17.0.8-5 to fix CVE-2023-21937, CVE-2023-21938, CVE-2023-21930, CVE-2023-21968, CVE-2023-21967,
- CVE-2023-21939, CVE-2022-21360, CVE-2023-21843, CVE-2023-21835, CVE-2023-21954
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 17.0.6-3
- Bump version as a part of freetype2 upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 17.0.6-2
- Bump version as a part of zlib upgrade
* Mon Feb 20 2023 Mukul Sikka <msikka@vmware.com> 17.0.6-1
- changing source name convention from openjdk-VERSION to jdk-VERSION
* Sat Feb 11 2023 Shreenidhi Shedi <sshedi@vmware.com> 17.0.5-3
- Bump version as a part of icu upgrade
* Fri Jan 06 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 17.0.5-2
- Bump up due to change in elfutils
* Fri Oct 28 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 17.0.5-1
- Update to tag jdk-17.0.5-ga
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
