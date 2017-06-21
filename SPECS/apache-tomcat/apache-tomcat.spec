Summary:	Apache Tomcat
Name:		apache-tomcat
Version:	8.5.15
Release:	2%{?dist}
License:	Apache
URL:		http://tomcat.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      noarch
Source0:    http://apache.mirrors.ionfish.org/tomcat/tomcat-8/v%{version}/src/%{name}-%{version}-src.tar.gz
%define sha1 apache-tomcat=5f26f71a1a3730020254a76aca1ee2615bd12d02
BuildRequires: openjre8
BuildRequires: openjdk8
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

%prep
%setup -qn %{name}-%{version}-src
# remove pre-built binaries and windows files
find . -type f \( -name "*.bat" -o -name "*.class" -o -name Thumbs.db -o -name "*.gz" -o \
   -name "*.jar" -o -name "*.war" -o -name "*.zip" \) -delete

%build
mkdir -p -m 700 %{_prefix}
ant -Dbase.path="." deploy dist-prepare dist-source javadoc

%install
mkdir -p -m 700 %{buildroot}%{_prefix}
mkdir -p -m 700 %{buildroot}%{_bindir}
mkdir -p -m 700 %{buildroot}%{_libdir}
mkdir -p -m 700 %{buildroot}%{_confdir}
mkdir -p -m 700 %{buildroot}%{_webappsdir}
mkdir -p -m 700 %{buildroot}%{_logsdir}
mkdir -p -m 700 %{buildroot}%{_tempdir}
cp -r %{_builddir}/%{name}-%{version}-src/output/build/bin/* %{buildroot}%{_bindir}
cp -r %{_builddir}/%{name}-%{version}-src/output/build/lib/* %{buildroot}%{_libdir}
cp -r %{_builddir}/%{name}-%{version}-src/output/build/conf/* %{buildroot}%{_confdir}
cp -r %{_builddir}/%{name}-%{version}-src/output/build/webapps/* %{buildroot}%{_webappsdir}

cp %{_builddir}/%{name}-%{version}-src/LICENSE %{buildroot}%{_prefix}
cp %{_builddir}/%{name}-%{version}-src/NOTICE %{buildroot}%{_prefix}

touch %{buildroot}%{_logsdir}/catalina.out
rm -rf %{buildroot}%{_prefix}/webapps/examples
rm -rf %{buildroot}%{_prefix}/webapps/docs

mkdir -p %{buildroot}%{_datadir}/java/tomcat

for jar in %{buildroot}/%{_libdir}/*.jar
do
    jarname=$(basename $jar .jar)
    ln -sfv %{_libdir}/${jarname}.jar %{buildroot}%{_datadir}/java/tomcat/${jarname}.jar
done

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%dir %{_prefix}
%dir %{_bindir}
%dir %{_libdir}
%dir %{_confdir}
%dir %{_webappsdir}
%dir %{_logsdir}
%dir %{_tempdir}
%{_bindir}/*
%{_confdir}/*
%{_libdir}/*
%{_webappsdir}/*
%{_datadir}/java/tomcat/*.jar
%{_prefix}/LICENSE
%{_prefix}/NOTICE
%{_logsdir}/catalina.out

%changelog
*   Tue Jun 20 2017 Divya Thaluru <dthaluru@vmware.com> 8.5.15-2
-   Removed version from directory path
-   Removed dependency on ANT_HOME
*   Tue Jun 6 2017 Divya Thaluru <dthaluru@vmware.com> 8.5.15-1
-   Upgraded to version 8.5.15
*   Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 8.5.13-3
-   Renamed openjdk to openjdk8
*   Tue Apr 18 2017 Divya Thaluru <dthaluru@vmware.com> 8.5.13-2
-   Added logic to package directories
*   Mon Apr 10 2017 Divya Thaluru <dthaluru@vmware.com> 8.5.13-1
-   Upgraded to version 8.5.13 and also added logic to build binaries from source
*   Tue Nov 22 2016 Anish Swaminathan <anishs@vmware.com> 8.5.8-1
-   Upgraded to version 8.5.8
*   Wed Oct 05 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.0.37-1
-   Update to version 8.0.37. Change openjre requires to latest
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 8.0.35-2
-   GA - Bump release of all rpms
*   Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> 8.0.35-1
-   Upgraded to version 8.0.35
*   Tue May 03 2016 Anish Swaminathan <anishs@vmware.com> 8.0.33-1
-   Upgraded to version 8.0.33
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 7.0.68-1
-   Upgraded to version 7.0.68
*   Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 7.0.63-3
-   Change path to /var/opt.
*   Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 7.0.63-2
-   Updated dependency after repackaging openjdk. 
*   Wed Jul 8 2015 Sriram Nambakam <snambakam@vmware.com> 7.0.63
-   Initial build.	First version
