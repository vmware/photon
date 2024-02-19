Summary:        Apache Tomcat
Name:           apache-tomcat
Version:        8.5.96
Release:        1%{?dist}
License:        Apache
URL:            http://tomcat.apache.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://archive.apache.org/dist/tomcat/tomcat-8/v%{version}/src/%{name}-%{version}-src.tar.gz
%define sha512 %{name}=3d2652e06d81eb014623bf1b0f03c238f330487682a255a4ed37a2b722f99194d08e3083b491d962917bc21cfbefd44f0e7808248c6b90c6a87db292138144dd

# Please check the below link for the supported java version
# https://tomcat.apache.org/whichversion.html
# base-for-apache-tomcat is a cached -Dbase.path folder
# generate base-for-apache-tomcat code with following steps:
# 1. tar -xvzf Source0 to $HOME
# 2. cd %{name}-%{version}-src && ant deploy dist-prepare dist-source
# 3. generated code will be exist to default location $HOME/tomcat-build-libs
# 4. mv tomcat-build-libs base-for-%{name}-%{version}
# 5. tar -cvzf base-for-%{name}-%{version}.tar.gz base-for-%{name}-%{version}
Source1: base-for-%{name}-%{version}.tar.gz
%define sha512 base=70bf85ebd014c1be306b1237a77400a0655b2455df099e84c314b277151ea8cdcb4d8c8d4603019be5e00f2870f8e0810f7e8c3365c95a10b3b4f69e8fb4794e

Patch0: apache-tomcat-use-jks-as-inmem-keystore.patch

BuildArch: noarch

BuildRequires: openjdk11
BuildRequires: apache-ant

Requires: openjre8
Requires: apache-ant

%define _prefix /var/opt/%{name}
%define _bindir %{_prefix}/bin
%define _confdir %{_prefix}/conf
%define _libdir %{_prefix}/lib
%define _webappsdir %{_prefix}/webapps
%define _logsdir %{_prefix}/logs
%define _tempdir %{_prefix}/temp

%description
The Apache Tomcat package contains binaries for the Apache Tomcat servlet container.

%package        webapps
Summary:        Web application for Apache Tomcat
Group:          Applications/System
Requires:       apache-tomcat = %{version}-%{release}
Conflicts:      apache-tomcat <= 8.5.84-1

%description    webapps
The web application for Apache Tomcat.

%prep
%autosetup -n %{name}-%{version}-src -N
# remove pre-built binaries and windows files
find . -type f \( -name "*.bat" -o -name "*.class" -o -name Thumbs.db -o -name "*.gz" -o \
   -name "*.jar" -o -name "*.war" -o -name "*.zip" \) -delete
%autosetup -D -b 1 -n %{name}-%{version}-src -p1

%build
ant -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8 \
 -Dbase.path="../base-for-%{name}-%{version}" deploy dist-prepare dist-source

%install
install -vdm 755 %{buildroot}%{_prefix}
install -vdm 755 %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_libdir}
install -vdm 755 %{buildroot}%{_confdir}
install -vdm 755 %{buildroot}%{_webappsdir}
install -vdm 755 %{buildroot}%{_logsdir}
install -vdm 755 %{buildroot}%{_tempdir}
cp -r %{_builddir}/%{name}-%{version}-src/output/build/bin/* %{buildroot}%{_bindir}
cp -r %{_builddir}/%{name}-%{version}-src/output/build/lib/* %{buildroot}%{_libdir}
cp -r %{_builddir}/%{name}-%{version}-src/output/build/conf/* %{buildroot}%{_confdir}
cp -r %{_builddir}/%{name}-%{version}-src/output/build/webapps/* %{buildroot}%{_webappsdir}

cp %{_builddir}/%{name}-%{version}-src/LICENSE %{buildroot}%{_prefix}
cp %{_builddir}/%{name}-%{version}-src/NOTICE %{buildroot}%{_prefix}

touch %{buildroot}%{_logsdir}/catalina.out
rm -rf %{buildroot}%{_prefix}/webapps/examples
rm -rf %{buildroot}%{_prefix}/webapps/docs

install -vdm 644 %{buildroot}%{_datadir}/java/tomcat

pushd %{buildroot}
for jar in ./%{_libdir}/*.jar; do
  jarname=$(basename $jar)
  ln -sfrv ./%{_libdir}/${jarname} ./%{_datadir}/java/tomcat/${jarname}
done
popd

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%dir %{_prefix}
%dir %{_bindir}
%dir %{_libdir}
%dir %{_confdir}
%dir %{_webappsdir}
%dir %{_webappsdir}/ROOT
%dir %{_logsdir}
%dir %{_tempdir}
%{_bindir}/*
%config(noreplace) %{_confdir}/catalina.policy
%config(noreplace) %{_confdir}/catalina.properties
%config(noreplace) %{_confdir}/context.xml
%config(noreplace) %{_confdir}/jaspic-providers.xml
%config(noreplace) %{_confdir}/jaspic-providers.xsd
%config(noreplace) %{_confdir}/logging.properties
%config(noreplace) %{_confdir}/server.xml
%config(noreplace) %{_confdir}/tomcat-users.xml
%config(noreplace) %{_confdir}/tomcat-users.xsd
%config(noreplace) %{_confdir}/web.xml
%{_libdir}/*
%dir %{_datadir}/java
%dir %{_datadir}/java/tomcat
%{_datadir}/java/tomcat/*.jar
%{_prefix}/LICENSE
%{_prefix}/NOTICE
%{_logsdir}/catalina.out

%files webapps
%defattr(-,root,root)
%dir %{_webappsdir}/manager
%dir %{_webappsdir}/host-manager
%{_webappsdir}/ROOT/*
%{_webappsdir}/manager/*
%{_webappsdir}/host-manager/*

%changelog
* Wed Feb 21 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 8.5.96-1
- Upgrade to 8.5.96, Fix CVE-2023-46589
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 8.5.88-2
- Bump version as a part of openjdk8 upgrade
* Wed Jun 14 2023 Nitesh Kumar <kunitesh@vmware.com> 8.5.88-1
- Upgrade to v8.5.88 to address CVE-2023-28709
* Tue May 16 2023 Nitesh Kumar <kunitesh@vmware.com> 8.5.86-1
- Upgrade to v8.5.86 to address CVE-2023-28708
* Thu Feb 16 2023 Prashant <psinghchauha@vmware.com> 8.5.84-2
- Package webapps as a subpackage
* Wed Jan 11 2023 Nitesh Kumar <kunitesh@vmware.com> 8.5.84-1
- Fix CVE-2022-42252, CVE-2022-45143
* Mon Jun 20 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5.78-2
- Fix CVE-2022-29885
* Mon Apr 04 2022 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5.78-1
- Update version to 8.5.78
* Thu Feb 10 2022 Nitesh Kumar <kunitesh@vmware.com> 8.5.72-2
- Fix CVE-2022-23181
* Fri Oct 29 2021 Dweep Advani <dadvani@vmware.com> 8.5.72-1
- Upgrade to 8.5.72 to address CVE-2021-42340
* Thu Sep 30 2021 Nitesh Kumar <kunitesh@vmware.com> 8.5.60-4
- Fix CVE-2021-41079
* Fri Jul 23 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5.60-3
- Fix CVE-2021-33037
* Mon Mar 08 2021 Dweep Advani <dadvani@vmware.com> 8.5.60-2
- Patched for CVE-2021-25122 and CVE-2021-25329
* Wed Dec 16 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5.60-1
- Update to version 8.5.60
* Thu Nov 05 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5.51-5
- Fix CVE-2020-13943
* Fri Jul 17 2020 Dweep Advani <dadvani@vmware.com> 8.5.51-4
- Patched for CVE-2020-13934 and CVE-2020-13935
* Mon Jul 06 2020 Dweep Advani <dadvani@vmware.com> 8.5.51-3
- Patched for CVE-2020-11996
* Wed May 27 2020 Dweep Advani <dadvani@vmware.com> 8.5.51-2
- Patched for CVE-2020-9484
* Mon Mar 09 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5.51-1
- Update to version 8.5.51 to fix CVE-2020-1938
* Fri Jan 03 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5.50-1
- Update to version 8.5.50 to fix CVE-2019-17563
* Tue Oct 01 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 8.5.46-1
- Update to version 8.5.46
* Thu Jul 04 2019 Dweep Advani <dadvani@vmware.com> 8.5.40-2
- Fix CVE-2019-10072
* Fri Apr 19 2019 Dweep Advani <dadvani@vmware.com> 8.5.40-1
- Upgrade to version 8.5.40
* Thu Jan 10 2019 Dweep Advani <dadvani@vmware.com> 8.5.37-1
- Upgrade to version 8.5.37
* Fri Dec 07 2018 Dweep Advani <dadvani@vmware.com> 8.5.35-1
- Upgrade to version 8.5.35
* Wed Nov 21 2018 Dweep Advani <dadvani@vmware.com> 8.5.31-3
- Fix CVE-2018-8014
* Thu May 17 2018 Xiaolin Li <xiaolinl@vmware.com> 8.5.31-2
- Mark configuration files as config(noreplace)
* Mon May 07 2018 Xiaolin Li <xiaolinl@vmware.com> 8.5.31-1
- Upgraded to version 8.5.31
* Mon Apr 30 2018 Xiaolin Li <xiaolinl@vmware.com> 8.5.30-1
- Upgraded to version 8.5.30
* Tue Mar 20 2018 Xiaolin Li <xiaolinl@vmware.com> 8.5.29-1
- Upgraded to version 8.5.29
* Wed Feb 28 2018 Xiaolin Li <xiaolinl@vmware.com> 8.5.28-1
- Upgraded to version 8.5.28
* Fri Feb 02 2018 Xiaolin Li <xiaolinl@vmware.com> 8.5.27-1
- Upgraded to version 8.5.27
* Thu Dec 21 2017 Anish Swaminathan <anishs@vmware.com> 8.5.24-1
- Upgraded to version 8.5.24
* Mon Oct 16 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.5.23-2
- patch to keep using inmem keystore as jks.
* Tue Oct 10 2017 Anish Swaminathan <anishs@vmware.com> 8.5.23-1
- Upgraded to version 8.5.23
* Wed Sep 27 2017 Alexey Makhalov <amakhalov@vmware.com> 8.5.20-3
- Offline build, disable javadoc target
* Wed Sep 13 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 8.5.20-2
- Updated the permissions on directories packaged
* Tue Aug 15 2017 Anish Swaminathan <anishs@vmware.com> 8.5.20-1
- Upgraded to version 8.5.20
* Thu Jul 6 2017 Divya Thaluru <dthaluru@vmware.com> 8.5.16-1
- Upgraded to version 8.5.16
* Tue Jun 20 2017 Divya Thaluru <dthaluru@vmware.com> 8.5.15-2
- Removed version from directory path
- Removed dependency on ANT_HOME
* Tue Jun 6 2017 Divya Thaluru <dthaluru@vmware.com> 8.5.15-1
- Upgraded to version 8.5.15
* Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 8.5.13-3
- Renamed openjdk to openjdk8
* Tue Apr 18 2017 Divya Thaluru <dthaluru@vmware.com> 8.5.13-2
- Added logic to package directories
* Mon Apr 10 2017 Divya Thaluru <dthaluru@vmware.com> 8.5.13-1
- Upgraded to version 8.5.13 and also added logic to build binaries from source
* Tue Nov 22 2016 Anish Swaminathan <anishs@vmware.com> 8.5.8-1
- Upgraded to version 8.5.8
* Wed Oct 05 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.0.37-1
- Update to version 8.0.37. Change openjre requires to latest
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.0.35-2
- GA - Bump release of all rpms
* Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 8.0.35-1
- Upgraded to version 8.0.35
* Tue May 03 2016 Anish Swaminathan <anishs@vmware.com> 8.0.33-1
- Upgraded to version 8.0.33
* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 7.0.68-1
- Upgraded to version 7.0.68
* Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 7.0.63-3
- Change path to /var/opt.
* Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 7.0.63-2
- Updated dependency after repackaging openjdk.
* Wed Jul 8 2015 Sriram Nambakam <snambakam@vmware.com> 7.0.63
- Initial build.  First version
