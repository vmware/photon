Summary:	Ant contrib
Name:		ant-contrib
Version:	1.0b3
Release:	15%{?dist}
License:	Apache
URL:		http://ant-contrib.sourceforget.net
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      noarch
Source0:	https://packages.vmware.com/photon/photon_sources/1.0/%{name}-%{version}-src.tar.gz
%define sha1 ant-contrib=b28d2bf18656b263611187fa9fbb95cec93d47c8
Patch0:         use-system-provided-commons-httpclient-jar.patch
BuildRequires: openjre8
BuildRequires: openjdk8
BuildRequires: apache-ant
BuildRequires: commons-httpclient
Requires: openjre8
Requires: apache-ant
%define _prefix /var/opt/ant-contrib

%description
The Ant Contrib project is a collection of tasks for Apache Ant.

%prep
%setup -n %{name}
%patch0 -p1
# Use system provided commons-httpclient jar instead of bundled one
find . -name '*.jar' -or -name '*.class' -exec rm -rf {} +
cp %{_datadir}/java/commons-httpclient/commons-httpclient.jar lib/commons-httpclient/jars/commons-httpclient-3.1.jar

%clean
rm -rf %{buildroot}

%build
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
ant -Ddist.dir="." -Dproject.version=%{version} dist

%install
export JAVA_HOME=`echo /usr/lib/jvm/OpenJDK*`
mkdir -p -m 700 %{buildroot}/var/opt
cd %{buildroot}/var/opt && tar xvzf %{_builddir}/%{name}/%{name}-%{version}-bin.tar.gz --wildcards "*.jar"

%files
%defattr(-,root,root)
%dir %{_prefix}
%dir %{_prefix}/lib
%{_prefix}/*.jar
%{_prefix}/lib/*.jar

%changelog
*   Thu Sep 10 2020 Ankit Jain <ankitja@vmware.com> 1.0b3-15
-   Use systems commons-httpclient
*   Fri Apr 24 2020 Ankit Jain <ankitja@vmware.com> 1.0b3-14
-   Changed openjdk install directory name
*   Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 1.0b3-13
-   Removed dependency on JAVA8_VERSION macro
*   Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 1.0b3-12
-   Removed dependency on ANT_HOME
*   Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0b3-11
-   Renamed openjdk to openjdk8
*   Fri Apr 07 2017 Divya Thaluru <dthaluru@vmware.com> 1.0b3-10
-   Removed prebuilt binaries from source tar ball
*   Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0b3-9
-   Updated JAVA_HOME path to point to latest.
*   Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0b3-8
-   Updated JAVA_HOME path to point to latest.
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0b3-7
-	GA - Bump release of all rpms
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
