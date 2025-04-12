%define _use_internal_dependency_generator 0
%define _origname   apache-tomcat
%define _prefix     %{_var}/opt/%{name}
%define _origprefix %{_var}/opt/%{_origname}
%define _bindir     %{_prefix}/bin
%define _confdir    %{_prefix}/conf
%define _libdir     %{_prefix}/lib
%define _webappsdir %{_prefix}/webapps
%define _logsdir    %{_prefix}/logs
%define _tempdir    %{_prefix}/temp

Summary:        Apache Tomcat 9
Name:           apache-tomcat9
Version:        9.0.98
Release:        3%{?dist}
License:        Apache
URL:            http://tomcat.apache.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://archive.apache.org/dist/tomcat/tomcat-9/v%{version}/src/%{_origname}-%{version}-src.tar.gz
%define sha512 %{_origname}=eb380dae515a259d23d5311d0b96b8ef5068c0d8d72da215410e5475582d2ff82182b7331e0d197eb993d8014a99ea40290154a343e961a07ed02be6894759cc

# Please check the below link for the supported java version
# https://tomcat.apache.org/whichversion.html
# base-for-apache-tomcat is a cached -Dbase.path folder
# generate base-for-apache-tomcat code with following steps:
# 1. tar -xvzf Source0 to $HOME
# 2. cd %{_origname}-%{version}-src && ant deploy dist-prepare dist-source
# 3. generated code will be exist to default location $HOME/tomcat-build-libs
# 4. mv tomcat-build-libs base-for-%{_origname}-%{version}
# 5. tar -cvzf base-for-%{_origname}-%{version}.tar.gz base-for-%{_origname}-%{version}
Source1: base-for-%{_origname}-%{version}.tar.gz
%define sha512 base=c6e718f37fc71247459e3932313931ef53ec1c8276a70b791ac9982702dcfae17c2670ab235c9b2cb905e6b9c71c6c3b6653f8bc827f8aaae1a8f9603eed2b07

Patch0: apache-tomcat-use-jks-as-inmem-keystore.patch
Patch1: apache-tomcat9-CVE-2025-24813.patch

BuildArch: noarch

BuildRequires: openjdk17
BuildRequires: apache-ant

Requires:         (openjre8 or openjdk11-jre or openjdk17-jre)
Requires:         apache-ant
Requires:         chkconfig
Requires(postun): chkconfig
Conflicts:        apache-tomcat <= 9.0.82-1%{?dist}

%description
The Apache Tomcat package contains binaries for the Apache Tomcat servlet container.

%package        webapps
Summary:        Web application for Apache Tomcat
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}
Conflicts:      apache-tomcat-webapps <= 9.0.82-1%{?dist}

%description    webapps
The web application for Apache Tomcat.

%prep
%autosetup -n %{_origname}-%{version}-src -p1 -b1
# remove pre-built binaries and windows files
find . -type f \( -name "*.bat" -o -name "*.class" -o -name Thumbs.db -o -name "*.gz" -o \
   -name "*.jar" -o -name "*.war" -o -name "*.zip" \) -delete

pushd %{_builddir}/base-for-%{_origname}-%{version}
mv tomcat-build-libs/* .
popd

%build
ant -Dant.build.javac.source=1.8 -Dant.build.javac.target=1.8 \
 -Dbase.path="../base-for-%{_origname}-%{version}" deploy dist-prepare dist-source

%install
install -vdm 755 %{buildroot}%{_prefix}
install -vdm 755 %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_libdir}
install -vdm 755 %{buildroot}%{_confdir}
install -vdm 755 %{buildroot}%{_webappsdir}
install -vdm 755 %{buildroot}%{_logsdir}
install -vdm 755 %{buildroot}%{_tempdir}
cp -a -r %{_builddir}/%{_origname}-%{version}-src/output/build/bin/* %{buildroot}%{_bindir}
cp -a -r %{_builddir}/%{_origname}-%{version}-src/output/build/lib/* %{buildroot}%{_libdir}
cp -a -r %{_builddir}/%{_origname}-%{version}-src/output/build/conf/* %{buildroot}%{_confdir}
cp -a -r %{_builddir}/%{_origname}-%{version}-src/output/build/webapps/* %{buildroot}%{_webappsdir}

cp -a %{_builddir}/%{_origname}-%{version}-src/LICENSE %{buildroot}%{_prefix}
cp -a %{_builddir}/%{_origname}-%{version}-src/NOTICE %{buildroot}%{_prefix}

touch %{buildroot}%{_logsdir}/catalina.out
rm -rf %{buildroot}%{_prefix}/webapps/{examples,docs}

install -vdm 644 %{buildroot}%{_datadir}/java/tomcat9

pushd %{buildroot}
for jar in ./%{_libdir}/*.jar; do
  jarname=$(basename $jar)
  ln -sfrv ./%{_libdir}/${jarname} ./%{_datadir}/java/tomcat9/${jarname}
done
popd

%clean
rm -rf %{buildroot}/*

%post
alternatives --install %{_origprefix} apache-tomcat %{_prefix} 10000 \
  --slave %{_datadir}/java/tomcat tomcat %{_datadir}/java/tomcat9

%postun
# Do alternative remove only in case of uninstall
if [ $1 -eq 0 ]; then
  alternatives --remove apache-tomcat %{_prefix}
fi

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
%dir %{_datadir}/java/tomcat9
%{_datadir}/java/tomcat9/*.jar
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
* Sat Apr 12 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 9.0.98-3
- Fix build regression
* Wed Apr 02 2025 Harinadh Dommaraju <harinadh.dommaraju@broadcom.com> 9.0.98-2
- Fix for CVE-2025-24813
* Thu Jan 02 2025 Harinadh D <harinadh.dommaraju@broadcom.com> 9.0.98-1
- Version upgrade to v9.0.98
- Fix for CVE-2024-50379,CVE-2024-54677,CVE-2024-56337
* Wed Nov 13 2024 Mukul Sikka <mukul.sikka@broadcom.com> 9.0.97-1
- Version upgrade to v9.0.97
* Tue Mar 19 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 9.0.86-1
- Version upgrade to v9.0.86
* Mon Mar 11 2024 Harinadh D <Harinadh.Dommaraju@broadcom.com> 9.0.83-2
- Version bump to use new jdk11 or jdk17
* Wed Feb 21 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 9.0.83-1
- Upgrade to 9.0.83, Fix CVE-2023-46589
* Tue Feb 20 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 9.0.82-2
- Fix file packaging
* Wed Nov 22 2023 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 9.0.82-1
- Add tomcat 9
