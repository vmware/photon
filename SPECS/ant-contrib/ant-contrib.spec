Summary:	Ant contrib
Name:		ant-contrib
Version:	1.0b3
Release:	3%{?dist}
License:	Apache
URL:		http://ant-contrib.sourceforget.net
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
BuildArch:      noarch
Source0:	http://dl.bintray.com/vmware/photon_release_1.0_TP1_x86_64/%{name}-%{version}-src.tar.gz
%define sha1 ant-contrib=b28d2bf18656b263611187fa9fbb95cec93d47c8
Requires: openjre >= 1.8.0.45, apache-ant >= 1.9.4
BuildRequires: openjre >= 1.8.0.45, apache-ant >= 1.9.4
BuildRequires: openjdk >= 1.8.0.45
%define _prefix /var/opt/ant-contrib

%description
The Ant Contrib project is a collection of tasks for Apache Ant.

%prep

%setup -n %{name}
%build
ANT_HOME=/var/opt/apache-ant-1.9.4
export JAVA_HOME=/var/opt/OpenJDK-1.8.0.51-bin
mkdir -p -m 700 %{_prefix}
$ANT_HOME/bin/ant -Ddist.dir="%{_prefix}" -Dproject.version="1.0b3" dist
%install
ANT_HOME=/var/opt/apache-ant-1.9.4
ANT_CONTRIB_DIST_DIR=%{buildroot}%{name}-%{version}
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
mkdir -p -m 700 %{buildroot}/var/opt
cd %{buildroot}/var/opt && tar xvzf %{_prefix}/ant-contrib-1.0b3-bin.tar.gz --wildcards "*.jar"
%files
%defattr(-,root,root)
%{_prefix}/*.jar
%{_prefix}/lib/*.jar

%changelog
*   Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 1.0b3.0-2
-	Change path to /var/opt.
*   Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0b3.0-1
-	Updated dependencies after repackaging openjdk. 
*   Tue Jun 9 2015 Sriram Nambakam <snambakam@vmware.com> 1.0b3.0-0
-   Initial commit
