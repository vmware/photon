%define _origname   apache-tomcat
%define _prefix     %{_var}/opt/%{name}
%define _origprefix %{_var}/opt/%{_origname}
%define _bindir     %{_prefix}/bin
%define _confdir    %{_prefix}/conf
%define _libdir     %{_prefix}/lib
%define _webappsdir %{_prefix}/webapps
%define _logsdir    %{_prefix}/logs
%define _tempdir    %{_prefix}/temp

Summary:        Apache Tomcat 11
Name:           apache-tomcat11
Version:        11.0.21
Release:        1%{?dist}
URL:            http://tomcat.apache.org
Group:          Applications/System
Vendor:         VMware, Inc.
BuildArch:      noarch
Distribution:   Photon

Obsoletes:      %{_origname} < 11.0.21-1%{?dist}
Provides:       %{_origname} = %{version}-%{release}

Source0: https://archive.apache.org/dist/tomcat/tomcat-11/v%{version}/src/%{_origname}-%{version}-src.tar.gz

# Please check the below link for the supported java version
# https://tomcat.apache.org/whichversion.html
#
# base-for-apache-tomcat is a cached -Dbase.path folder
# Generate base-for-apache-tomcat code with following steps:
# 1. tar -xvzf Source0 to $HOME
# 2. cd %{_origname}-%{version}-src && ant deploy dist-prepare dist-source
# 3. generated code will be exist to default location $HOME/tomcat-build-libs
# 4. delete nsis-3.11-src.tar.bz2, nsis-3.11.zip and download-211133185.zip
#    present inside $HOME/tomcat-build-libs.(version number may differ)
# 4. mv tomcat-build-libs base-for-%{_origname}-%{version}
# 5. tar -cvzf base-for-%{_origname}-%{version}.tar.gz base-for-%{_origname}-%{version}
Source1: base-for-%{_origname}-%{version}.tar.gz

Source2: license-apache-tomcat11.txt
%include %{SOURCE2}

BuildRequires: openjdk17
BuildRequires: apache-ant

Requires:         jre >= 17.0
Requires:         apache-ant
Requires:         alternatives
Requires(postun): alternatives

%description
The Apache Tomcat package contains binaries for the Apache Tomcat servlet container.

%package        webapps
Summary:        Web application for Apache Tomcat
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{_origname}-webapps < 11.0.21-1%{?dist}
Provides:       %{_origname}-webapps = %{version}-%{release}

%description    webapps
The web application for Apache Tomcat.

%prep
%autosetup -n %{_origname}-%{version}-src -p1 -b1
# remove pre-built binaries and windows files
find . -type f \( -name "*.bat" -o -name "*.class" -o -name Thumbs.db -o -name "*.gz" -o \
   -name "*.jar" -o -name "*.war" -o -name "*.zip" \) -delete

%build
ant \
  -Dant.build.javac.source=17 \
  -Dant.build.javac.target=17 \
  -Dbase.path="../base-for-%{_origname}-%{version}" \
  deploy dist-prepare dist-source

%install
install -vdm 755 %{buildroot}%{_prefix}
install -vdm 755 %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_libdir}
install -vdm 755 %{buildroot}%{_confdir}
install -vdm 755 %{buildroot}%{_webappsdir}
install -vdm 755 %{buildroot}%{_logsdir}
install -vdm 755 %{buildroot}%{_tempdir}
cp -a %{_builddir}/%{_origname}-%{version}-src/output/build/bin/* %{buildroot}%{_bindir}
cp -a %{_builddir}/%{_origname}-%{version}-src/output/build/lib/* %{buildroot}%{_libdir}
cp -a %{_builddir}/%{_origname}-%{version}-src/output/build/conf/* %{buildroot}%{_confdir}
cp -a %{_builddir}/%{_origname}-%{version}-src/output/build/webapps/* %{buildroot}%{_webappsdir}

cp -a %{_builddir}/%{_origname}-%{version}-src/LICENSE %{buildroot}%{_prefix}
cp -a %{_builddir}/%{_origname}-%{version}-src/NOTICE %{buildroot}%{_prefix}

touch %{buildroot}%{_logsdir}/catalina.out
rm -rf %{buildroot}%{_prefix}/webapps/{examples,docs}

install -vdm 644 %{buildroot}%{_datadir}/java/tomcat11

pushd %{buildroot}
for jar in ./%{_libdir}/*.jar; do
  jarname=$(basename $jar)
  ln -sfrv ./%{_libdir}/${jarname} ./%{_datadir}/java/tomcat11/${jarname}
done
popd

%clean
rm -rf %{buildroot}/*

%post
alternatives --install %{_origprefix} apache-tomcat %{_prefix} 20000 \
  --slave %{_datadir}/java/tomcat tomcat %{_datadir}/java/tomcat11

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
%dir %{_datadir}/java/tomcat11
%{_datadir}/java/tomcat11/*.jar
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
* Tue Apr 14 2026 Guruswamy Basavaiah <guruswamy.basavaiah@broadcom.com> 11.0.21-1
- Initial build of version 11.0.21
