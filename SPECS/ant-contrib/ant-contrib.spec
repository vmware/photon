Summary:	Ant contrib
Name:		ant-contrib
Version:	1.0b3
Release:	14%{?dist}
License:	Apache
URL:		http://ant-contrib.sourceforget.net
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      noarch
Source0:	http://dl.bintray.com/vmware/photon_release_1.0_TP1_x86_64/%{name}-%{version}-src.tar.gz
%define sha1 ant-contrib=b28d2bf18656b263611187fa9fbb95cec93d47c8
BuildRequires: openjre
BuildRequires: openjdk
BuildRequires: apache-ant
Requires: openjre
Requires: apache-ant
%define _prefix /var/opt/ant-contrib

%description
The Ant Contrib project is a collection of tasks for Apache Ant.

%prep
%setup -n %{name}
find . -name '*.jar' -or -name '*.class' -exec rm -rf {} +

%clean
rm -rf %{buildroot}

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-*`
ant -Ddist.dir="." -Dproject.version=%{version} dist

%install
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK-*`
mkdir -p -m 700 %{buildroot}/var/opt
cd %{buildroot}/var/opt && tar xvzf %{_builddir}/%{name}/%{name}-%{version}-bin.tar.gz --wildcards "*.jar"
%files
%defattr(-,root,root)
%dir %{_prefix}
%dir %{_prefix}/lib
%{_prefix}/*.jar
%{_prefix}/lib/*.jar

%changelog
*   Fri Mar 15 2019 Ankit Jain <ankitja@vmware.com> 1.0b3-14
-   Removed JAVA_VERSION macro
*   Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 1.0b3-13
-   Removed dependency on ANT_HOME
*   Fri May 19 2017 Harish Udiaya Kumar <hudaiyakumar@vmware.com> 1.0b3-12
-   Use java alternatives
*   Mon May 01 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0b3-11
-   Use java_macros to determine the version on updating java to 1.8.0.131
*   Fri Apr 07 2017 Divya Thaluru <dthaluru@vmware.com> 1.0b3-10
-   Removed prebuilt binaries from source tar ball
*   Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0b3-9
-   Updated JAVA_HOME path to point to latest.
*   Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0b3-8
-   Updated JAVA_HOME path to point to latest.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0b3-7
-   GA - Bump release of all rpms
*   Fri May 20 2016 Divya Thaluru<dthaluru@vmware.com> 1.0b3-6
-   Updated JAVA_HOME path to point to latest.
*   Wed Mar 02 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0b3.0-5
-   Updated apache-ant to version 1.9.6
*   Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0b3.0-4
-   Updated JAVA_HOME path to point to latest.
*   Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 1.0b3.0-2
-   Change path to /var/opt.
*   Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0b3.0-1
-   Updated dependencies after repackaging openjdk.
*   Tue Jun 9 2015 Sriram Nambakam <snambakam@vmware.com> 1.0b3.0-0
-   Initial commit
