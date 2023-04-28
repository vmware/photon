%define _use_internal_dependency_generator 0
%global security_hardening none
%define jdk_major_version 17

Summary:        OpenJDK
Name:           openjdk17
Version:        17.0.6
Release:        3%{?dist}
License:        GNU General Public License V2
URL:            https://openjdk.java.net
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:    https://github.com/openjdk/jdk17u/archive/refs/tags/jdk-%{version}-ga.tar.gz
%define sha512 jdk-17=7fa47285fb1776802dc35352bfe64d6b376cbc73d7b72ef7d5c8ad41c181d8aa9dc6fb392fe3b1c799974765d40c03a6643ad6afeb3ddc9ab45e546b747ebb3c

BuildArch:      aarch64
BuildRequires:  pcre-devel
BuildRequires:  which
BuildRequires:  zip
BuildRequires:  unzip
BuildRequires:  zlib-devel
BuildRequires:  ca-certificates
BuildRequires:  chkconfig
BuildRequires:  freetype2
BuildRequires:  fontconfig-devel
BuildRequires:  freetype2-devel
BuildRequires:  glib-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  elfutils-libelf-devel

Requires:       chkconfig
Requires:       libstdc++

AutoReqProv:    no

%define ExtraBuildRequires icu-devel, cups, cups-devel, openjdk17, libXtst, libXtst-devel, libXi, libXi-devel, icu, alsa-lib, alsa-lib-devel, xcb-proto, libXdmcp-devel, libXau-devel, util-macros, xtrans, libxcb-devel, proto, libXdmcp, libxcb, libXau, libX11, libX11-devel, libXext, libXext-devel, libXt, libXt-devel, libXrender, libXrender-devel, libXrandr, libXrandr-devel

%description
The OpenJDK package installs java class library and javac java compiler.

%package        doc
Summary:        Documentation and demo applications for openjdk
Group:          Development/Languages/Java
Requires:       %{name} = %{version}-%{release}
%description    doc
It contains the documentation and demo applications for openjdk

%package        src
Summary:        OpenJDK Java classes for developers
Group:          Development/Languages/Java
Requires:       %{name} = %{version}-%{release}
%description    src
This package provides the runtime library class sources.

%prep -p exit
%autosetup -p1 -n jdk17u-jdk-%{version}-ga

%build
chmod a+x ./configur*
unset JAVA_HOME
ENABLE_HEADLESS_ONLY="true"

./configur* \
        --with-target-bits=64 \
        --enable-headless-only \
        --with-extra-cxxflags="-Wno-error -fno-delete-null-pointer-checks -fno-lifetime-dse" \
        --with-extra-cflags="-fno-delete-null-pointer-checks -Wno-error -fno-lifetime-dse" \
        --with-freetype-include=%{_includedir}/freetype2 \
        --with-freetype-lib=%{_libdir} \
        --with-stdc++lib=dynamic \
        --disable-warnings-as-errors

mkdir %{_datadir}/java -p
# make doesn't support _smp_mflags
make \
    DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
    SCTP_WERROR= \
    BUILD_HEADLESS_ONLY=1 \
    OPENJDK_TARGET_OS=linux \
    STRIP_POLICY=no_strip \
    POST_STRIP_CMD="" \
    LOG=trace

%install
unset JAVA_HOME
# make doesn't support _smp_mflags
make install

install -vdm755 %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}
chown -R root:root %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}
install -vdm755 %{buildroot}%{_bindir}
mv %{_usr}/local/jvm/openjdk-%{version}-internal/* %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/
cp README.md LICENSE ASSEMBLY_EXCEPTION %{buildroot}%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/

%posttrans
alternatives --install %{_bindir}/javac javac %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javac 30000 \
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

alternatives --install %{_bindir}/java java %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/java 30000 \
  --slave %{_bindir}/jjs jjs %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jjs \
  --slave %{_bindir}/keytool keytool %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/keytool \
  --slave %{_bindir}/pack200 pack200 %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/pack200 \
  --slave %{_bindir}/rmid rmid %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/rmiregistry \
  --slave %{_bindir}/unpack200 unpack200 %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/unpack200
/sbin/ldconfig

%postun
# Do alternative remove only in case of uninstall
if [ $1 -eq 0 ]; then
  alternatives --remove javac %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/javac
  alternatives --remove java %{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/java
fi
/sbin/ldconfig

%clean
rm -rf %{buildroot}/* \
       %{_libdir}/jvm/OpenJDK-*

%files
%defattr(-,root,root)
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/ASSEMBLY_EXCEPTION
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/LICENSE
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/README.md
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/release
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/lib
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/include/
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
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/serialver
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/conf
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/jmods
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/java
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/keytool
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/rmiregistry
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jfr
%{_libdir}/jvm/OpenJDK-%{jdk_major_version}/bin/jpackage
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
* Tue Sep 20 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 11.0.12-3
- Fix build with latest toolchain
* Wed Sep 07 2022 Piyush Gupta <gpiyush@vmware.com> 11.0.12-2
- Fix for CVE-2022-34169.
* Mon Jun 27 2022 Prashant S Chauhan <psinghchauha@vmware.com> 11.0.12-1
- Initial build. First version
