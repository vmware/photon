%global security_hardening  none
%define jdk_major_version   1.8.0
%define subversion          502
%define _use_internal_dependency_generator 0
%define _jobs %(echo $(( ($(nproc)+1) / 2 )))
%define jdkInstallDir %{_libdir}/jvm/OpenJDK-%{jdk_major_version}

%ifarch x86_64
%define bootstrapjdkversion 1.8.0.112
%endif

%ifarch aarch64
%define bootstrapjdkversion 1.8.0.151
%endif

Summary:    OpenJDK
Name:       openjdk8
Version:    1.8.0.502
Release:    1%{?dist}
License:    GNU GPL
URL:        https://wiki.openjdk.org/display/jdk8u
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0: https://github.com/openjdk/jdk8u/archive/refs/tags/jdk8u%{subversion}-ga.tar.gz
%define sha512 jdk8u=fdcb0cc19cba5bb8cabfc3c6439ae5d1ce33d5fa500b1fe2a7b8152bedaacdda11e58fd2eb0357a815dfc1a44423023a9149409c0cdaac931fe0958e91bca343

Patch0: Awt_build_headless_only.patch
Patch1: check-system-ca-certs-x86.patch
Patch2: allow_using_system_installed_libjpeg.patch

BuildRequires: pcre-devel
BuildRequires: which
BuildRequires: zip
BuildRequires: unzip
BuildRequires: zlib-devel
BuildRequires: ca-certificates
BuildRequires: chkconfig
BuildRequires: libjpeg-turbo-devel
BuildRequires: fontconfig-devel
BuildRequires: freetype2-devel
BuildRequires: glib-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: libXrender-devel
BuildRequires: libxcb-devel
BuildRequires: libXrandr-devel
BuildRequires: libXtst-devel
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: cups-devel
BuildRequires: alsa-lib-devel

%ifarch aarch64
%define ExtraBuildRequires openjdk8, openjre8
%endif

%ifarch x86_64
%define ExtraBuildRequires openjdk, openjre
%endif

Requires: openjre8 = %{version}-%{release}
Requires: chkconfig

Obsoletes: openjdk <= %{version}

AutoReqProv: no

%description
The OpenJDK package installs java class library and javac java compiler.

%package -n openjre8
Summary:        Java runtime environment
AutoReqProv:    no
Obsoletes:      openjre <= %{version}
Requires:       chkconfig
Requires:       libstdc++
Provides:       jre = %{version}

%description    -n openjre8
It contains the libraries files for Java runtime environment

%package        sample
Summary:        Sample java applications.
Group:          Development/Languages/Java
Obsoletes:      openjdk-sample <= %{version}
Requires:       %{name} = %{version}-%{release}

%description    sample
It contains the Sample java applications.

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
%autosetup -p1 -n jdk8u-jdk8u%{subversion}-ga

rm jdk/src/solaris/native/sun/awt/CUPSfuncs.c
sed -i "s#\"ft2build.h\"#<ft2build.h>#g" jdk/src/share/native/sun/font/freetypeScaler.c
sed -i '0,/BUILD_LIBMLIB_SRC/s/BUILD_LIBMLIB_SRC/BUILD_HEADLESS_ONLY := 1\nOPENJDK_TARGET_OS := linux\n&/' jdk/make/lib/Awt2dLibraries.gmk

%build
pushd common/autoconf
bash ./autogen.sh
popd

unset JAVA_HOME

%ifarch x86_64
BOOT_JDK="%{_var}/opt/OpenJDK-%{bootstrapjdkversion}-bin"
%endif

%ifarch aarch64
BOOT_JDK="%{_libdir}/jvm/OpenJDK-%{bootstrapjdkversion}"
%endif

sh ./configure \
    CUPS_NOT_NEEDED=yes \
    --with-target-bits=64 \
    --with-boot-jdk=${BOOT_JDK} \
    --disable-headful \
    --with-extra-cxxflags="-Wno-error -std=gnu++98 -fno-delete-null-pointer-checks -fno-lifetime-dse" \
    --with-extra-cflags="-std=gnu++98 -fno-delete-null-pointer-checks -Wno-error -fno-lifetime-dse -fcommon" \
    --with-freetype-include=%{_includedir}/freetype2 \
    --with-freetype-lib=%{_libdir} \
    --with-stdc++lib=dynamic \
    --disable-zip-debug-info \
    --with-libjpeg=system

# make doesn't support _smp_mflags
make \
    DEBUG_BINARIES=true \
    BUILD_HEADLESS_ONLY=1 \
    OPENJDK_TARGET_OS=linux \
    JAVAC_FLAGS=-g \
    STRIP_POLICY=no_strip \
    DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
    CLASSPATH=${BOOT_JDK}/jre \
    POST_STRIP_CMD="" \
    LOG=trace \
    JOBS=%{_jobs} \
    SCTP_WERROR=

%install
# make doesn't support _smp_mflags
make DESTDIR=%{buildroot} install \
        JOBS=%{_jobs} \
        BUILD_HEADLESS_ONLY=yes \
        OPENJDK_TARGET_OS=linux \
        DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
        CLASSPATH=${BOOT_JDK}/jre

install -vdm755 %{buildroot}%{jdkInstallDir}
chown -R root:root %{buildroot}%{jdkInstallDir}
install -vdm755 %{buildroot}%{_bindir}

pushd %{_usr}/local/jvm/openjdk-%{jdk_major_version}_%{subversion}-internal/jre/lib
%ifarch x86_64
find amd64 -iname \*.diz -delete
%else
find aarch64 -iname \*.diz -delete
%endif
popd

mv %{_usr}/local/jvm/openjdk-%{jdk_major_version}_%{subversion}-internal/* \
            %{buildroot}%{jdkInstallDir}/

%post
alternatives --install %{_bindir}/javac javac %{jdkInstallDir}/bin/javac 2000 \
  --slave %{_bindir}/appletviewer appletviewer %{jdkInstallDir}/bin/appletviewer \
  --slave %{_bindir}/extcheck extcheck %{jdkInstallDir}/bin/extcheck \
  --slave %{_bindir}/idlj idlj %{jdkInstallDir}/bin/idlj \
  --slave %{_bindir}/jar jar %{jdkInstallDir}/bin/jar \
  --slave %{_bindir}/jarsigner jarsigner %{jdkInstallDir}/bin/jarsigner \
  --slave %{_bindir}/javadoc javadoc %{jdkInstallDir}/bin/javadoc \
  --slave %{_bindir}/javah javah %{jdkInstallDir}/bin/javah \
  --slave %{_bindir}/javap javap %{jdkInstallDir}/bin/javap \
  --slave %{_bindir}/jcmd jcmd %{jdkInstallDir}/bin/jcmd \
  --slave %{_bindir}/jconsole jconsole %{jdkInstallDir}/bin/jconsole \
  --slave %{_bindir}/jdb jdb %{jdkInstallDir}/bin/jdb \
  --slave %{_bindir}/jdeps jdeps %{jdkInstallDir}/bin/jdeps \
  --slave %{_bindir}/jhat jhat %{jdkInstallDir}/bin/jhat \
  --slave %{_bindir}/jinfo jinfo %{jdkInstallDir}/bin/jinfo \
  --slave %{_bindir}/jmap jmap %{jdkInstallDir}/bin/jmap \
  --slave %{_bindir}/jps jps %{jdkInstallDir}/bin/jps \
  --slave %{_bindir}/jrunscript jrunscript %{jdkInstallDir}/bin/jrunscript \
  --slave %{_bindir}/jsadebugd jsadebugd %{jdkInstallDir}/bin/jsadebugd \
  --slave %{_bindir}/jstack jstack %{jdkInstallDir}/bin/jstack \
  --slave %{_bindir}/jstat jstat %{jdkInstallDir}/bin/jstat \
  --slave %{_bindir}/jstatd jstatd %{jdkInstallDir}/bin/jstatd \
  --slave %{_bindir}/native2ascii native2ascii %{jdkInstallDir}/bin/native2ascii \
  --slave %{_bindir}/rmic rmic %{jdkInstallDir}/bin/rmic \
  --slave %{_bindir}/schemagen schemagen %{jdkInstallDir}/bin/schemagen \
  --slave %{_bindir}/serialver serialver %{jdkInstallDir}/bin/serialver \
  --slave %{_bindir}/wsgen wsgen %{jdkInstallDir}/bin/wsgen \
  --slave %{_bindir}/wsimport wsimport %{jdkInstallDir}/bin/wsimport \
  --slave %{_bindir}/xjc xjc %{jdkInstallDir}/bin/xjc \
  --slave %{_bindir}/jfr jfr %{jdkInstallDir}/bin/jfr
/sbin/ldconfig

%post -n openjre8
alternatives --install %{_bindir}/java java %{jdkInstallDir}/jre/bin/java 2000 \
  --slave %{_libdir}/jvm/jre jre %{jdkInstallDir}/jre \
  --slave %{_bindir}/jjs jjs %{jdkInstallDir}/jre/bin/jjs \
  --slave %{_bindir}/keytool keytool %{jdkInstallDir}/jre/bin/keytool \
  --slave %{_bindir}/orbd orbd %{jdkInstallDir}/jre/bin/orbd \
  --slave %{_bindir}/pack200 pack200 %{jdkInstallDir}/jre/bin/pack200 \
  --slave %{_bindir}/rmid rmid %{jdkInstallDir}/jre/bin/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{jdkInstallDir}/jre/bin/rmiregistry \
  --slave %{_bindir}/servertool servertool %{jdkInstallDir}/jre/bin/servertool \
  --slave %{_bindir}/tnameserv tnameserv %{jdkInstallDir}/jre/bin/tnameserv \
  --slave %{_bindir}/unpack200 unpack200 %{jdkInstallDir}/jre/bin/unpack200
/sbin/ldconfig

%postun
# Do alternative remove only in case of uninstall
if [ $1 -eq 0 ]; then
  alternatives --remove javac %{jdkInstallDir}/bin/javac
fi
/sbin/ldconfig

%postun -n openjre8
# Do alternative remove only in case of uninstall
if [ $1 -eq 0 ]; then
  alternatives --remove java %{jdkInstallDir}/jre/bin/java
fi
/sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{jdkInstallDir}/ASSEMBLY_EXCEPTION
%{jdkInstallDir}/LICENSE
%{jdkInstallDir}/release
%{jdkInstallDir}/THIRD_PARTY_README
%{jdkInstallDir}/lib
%{jdkInstallDir}/include/
%{jdkInstallDir}/bin/extcheck
%{jdkInstallDir}/bin/idlj
%{jdkInstallDir}/bin/jar
%{jdkInstallDir}/bin/jarsigner
%{jdkInstallDir}/bin/java-rmi.cgi
%{jdkInstallDir}/bin/javac
%{jdkInstallDir}/bin/javadoc
%{jdkInstallDir}/bin/javah
%{jdkInstallDir}/bin/javap
%{jdkInstallDir}/bin/jcmd
%{jdkInstallDir}/bin/jconsole
%{jdkInstallDir}/bin/jdb
%{jdkInstallDir}/bin/jdeps
%{jdkInstallDir}/bin/jhat
%{jdkInstallDir}/bin/jinfo
%{jdkInstallDir}/bin/jjs
%{jdkInstallDir}/bin/jmap
%{jdkInstallDir}/bin/jps
%{jdkInstallDir}/bin/jrunscript
%{jdkInstallDir}/bin/jsadebugd
%{jdkInstallDir}/bin/jstack
%{jdkInstallDir}/bin/jstat
%{jdkInstallDir}/bin/jstatd
%{jdkInstallDir}/bin/native2ascii
%{jdkInstallDir}/bin/rmic
%{jdkInstallDir}/bin/schemagen
%{jdkInstallDir}/bin/serialver
%{jdkInstallDir}/bin/wsgen
%{jdkInstallDir}/bin/wsimport
%{jdkInstallDir}/bin/xjc
%{jdkInstallDir}/bin/clhsdb
%{jdkInstallDir}/bin/hsdb
%{jdkInstallDir}/bin/jfr
%exclude %{jdkInstallDir}/bin/*.debuginfo

%files  -n openjre8
%defattr(-,root,root)
%dir %{jdkInstallDir}
%{jdkInstallDir}/jre/
%{jdkInstallDir}/bin/java
%{jdkInstallDir}/bin/keytool
%{jdkInstallDir}/bin/orbd
%{jdkInstallDir}/bin/pack200
%{jdkInstallDir}/bin/rmid
%{jdkInstallDir}/bin/rmiregistry
%{jdkInstallDir}/bin/servertool
%{jdkInstallDir}/bin/tnameserv
%{jdkInstallDir}/bin/unpack200
%ifarch x86_64
%{jdkInstallDir}/lib/amd64/jli/
%exclude %{jdkInstallDir}/lib/amd64/*.diz
%else
%{jdkInstallDir}/lib/aarch64/jli/
%endif

%files sample
%defattr(-,root,root)
%{jdkInstallDir}/sample/

%files doc
%defattr(-,root,root)
%{jdkInstallDir}/man/
%{jdkInstallDir}/demo

%files src
%defattr(-,root,root)
%{jdkInstallDir}/src.zip

%changelog
* Tue Aug 11 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.0.502-1
- Upgrade to v1.8.0.502
* Sun Jul 12 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.0.482-2
- Fix aarch64 build
* Tue Feb 10 2026 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.0.482-1
- Upgrade to v1.8.0.482
* Mon Oct 27 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.0.472-1
- Club aarch64 and amd64 specs
- This is also a prep change for ExtraBuildRequires removal from jdk specs
- Version upgrade contains a bunch of CVE fixes
* Wed Oct 08 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.0.462-2
- Build jdk8 with bundled cacerts
* Fri Aug 22 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.0.462-1
- Upgrade to v1.8.0.462
* Wed Jan 22 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.8.0.442-1
- Upgrade to v 1.8.0.442
* Tue Mar 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.8.0.402-1
- Upgrade to v1.8.0.402
* Sat Oct 07 2023 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.8.0.382-4
- Bump version as part of glib upgrade
* Fri Sep 29 2023 Srish Srinivasan <ssrish@vmware.com> 1.8.0.382-3
- Version bump as a part of cups upgrade
* Mon Jul 10 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.8.0.382-2
- Bump version as a part of cups upgrade
* Fri Jun 16 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.8.0.382-1
- Upgrade to v1.8.0.382
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 1.8.0.322-3
- Bump version as a part of freetype2 upgrade
* Thu Dec 22 2022 Mukul Sikka <msikka@vmware.com> 1.8.0.322-2
- fix post install script error “--slave: command not found”
* Mon Jul 04 2022 Piyush Gupta <gpiyush@vmware.com> 1.8.0.322-1
- Upgrade to version 1.8.0.322 (jdk8u322-b04)
* Wed May 18 2022 Ankit Jain <ankitja@vmware.com> 1.8.0.312-1
- Upgrade to version 1.8.0.312 (jdk8u312-ga)
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 1.8.0.265-2
- GCC-10 support.
* Tue Oct 06 2020 Tapas Kundu <tkundu@vmware.com> 1.8.0.265-1
- Upgrade to version 1.8.0.265 (jdk8u265-ga)
* Mon Oct 05 2020 Tapas Kundu <tkundu@vmware.com> 1.8.0.262-3
- Use libjpeg-turbo
- Fix CVE-2020-14153, CVE-2020-14152
* Tue Aug 11 2020 Ankit Jain <ankitja@vmware.com> 1.8.0.262-2
- Added a check in %postun to avoid alternatives --remove
- after new version is installed.
- Do alternative remove only in case of uninstall.
* Fri Jul 24 2020 Shreyas B <shreyasb@vmware.com> 1.8.0.262-1
- Upgrade to version 1.8.0.262 (jdk8u262-ga)
* Fri Apr 24 2020 Ankit Jain <ankitja@vmware.com> 1.8.0.252-2
- Cleaned removing of OpenJDK-1.8.0 directory in postun
* Fri Apr 17 2020 Tapas Kundu <tkundu@vmware.com> 1.8.0.252-1
- Upgrade to version 1.8.0.252 ga (jdk8u252-ga)
* Mon Apr 13 2020 Tapas Kundu <tkundu@vmware.com> 1.8.0.242-1
- Upgrade to version 1.8.0.242 ga (jdk8u242-ga)
* Fri Oct 25 2019 Shreyas B. <shreyasb@vmware.com> 1.8.0.232-1
- Upgrade to version 1.8.0.232 ga (jdk8u232-ga)
* Wed Sep 18 2019 Ankit Jain <ankitja@vmware.com> 1.8.0.222-2
- Divided version:majorversion+subversion to remove specific
- version java dependency from other packages
* Thu Aug 01 2019 Shreyas B. <shreyasb@vmware.com> 1.8.0.222-1
- Upgrade to version 1.8.0.222 b10 (jdk8u222-b10)
- Fix diff for TrustStoreManager.java in file check-system-ca-certs.patch to check-system-ca-certs-212-b04.patch.
- Replace check-system-ca-certs.patch with check-system-ca-certs-212-b04.patch to build x64-86 binary.
* Tue May 21 2019 Tapas Kundu <tkundu@vmware.com> 1.8.0.212-2
- Upgrade to version 1.8.0.212 b04
- Included fix for performance regression.
* Thu May 02 2019 Tapas Kundu <tkundu@vmware.com> 1.8.0.212-1
- Upgrade to version 1.8.0.212
- Add new clhsdb and hsdb binaries.
- Fix CVE-2019-2602, CVE-2019-2697, CVE-2019-2698.
* Wed Jan 23 2019 Srinidhi Rao <srinidhir@vmware.com> 1.8.0.202-1
- Upgrade to version 1.8.0.202
* Mon Oct 29 2018 Ajay Kaher <akaher@vmware.com> 1.8.0.192-3
- Adding BuildArch
* Mon Oct 29 2018 Alexey Makhalov <amakhalov@vmware.com> 1.8.0.192-2
- Use ExtraBuildRequires
* Thu Oct 18 2018 Tapas Kundu <tkundu@vmware.com> 1.8.0.192-1
- Upgraded to version 1.8.0.192
* Fri Sep 21 2018 Srinidhi Rao <srinidhir@vmware.com> 1.8.0.181-1
- Upgraded to 1.8.0.181 version.
* Mon Apr 23 2018 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.0.172-1
- Upgraded to version 1.8.0.172
* Fri Jan 19 2018 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.0.162-1
- Upgraded to version 1.8.0.162
* Thu Dec 21 2017 Alexey Makhalov <amakhalov@vmware.com> 1.8.0.152-2
- Reduce list of published rpms dependencies
* Thu Oct 19 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.0.152-1
- Upgraded to version 1.8.0.152
* Thu Sep 14 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.0.141-2
- added ldconfig in post actions.
* Fri Jul 21 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.0.141-1
- Upgraded to version 1.8.0.141-1
* Thu Jul 6 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.0.131-4
- Build AWT libraries as well.
* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> 1.8.0.131-3
- Added obseletes for deprecated openjdk package
* Tue Jun 06 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.0.131-2
- Add requires for libstdc++
* Mon Apr 10 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.0.131-1
- Upgraded to version 1.8.0.131 and building Java from sources
* Tue Mar 28 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.0.112-2
- add java rpm macros
* Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.0.112-1
- Update to 1.8.0.112. addresses CVE-2016-5582 CVE-2016-5573
* Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.0.102-1
- Update to 1.8.0.102, minor fixes in url, spelling.
- addresses CVE-2016-3598, CVE-2016-3606, CVE-2016-3610
* Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com> 1.8.0.92-3
- Added version constraint to runtime dependencies
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.0.92-2
- GA - Bump release of all rpms
* Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 1.8.0.92-1
- Updated to version 1.8.0.92
* Mon May 2 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.8.0.72-3
- Move tools like javac to openjdk
* Thu Apr 28 2016 Divya Thaluru <dthaluru@vmware.com> 1.8.0.72-2
- Adding openjre as run time dependency for openjdk package
* Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.8.0.72-1
- Updating Version.
* Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 1.8.0.51-3
- Change to use /var/opt path
* Fri Sep 11 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.8.0.51-2
- Split the openjdk into multiple sub-packages to reduce size.
* Mon Aug 17 2015 Sharath George <sarahc@vmware.com> 1.8.0.51-1
- Moved to the next version
* Tue Jun 30 2015 Sarah Choi <sarahc@vmware.com> 1.8.0.45-2
- Add JRE path
* Mon May 18 2015 Sharath George <sharathg@vmware.com> 1.8.0.45-1
- Initial build. First version
