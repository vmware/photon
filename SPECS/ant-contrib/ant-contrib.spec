%define _prefix %{_var}/opt/%{name}

Summary:    Ant contrib
Name:       ant-contrib
Version:    1.0b3
Release:    18%{?dist}
License:    Apache
URL:        http://ant-contrib.sourceforget.net
Group:      Applications/System
Vendor:     VMware, Inc.
Distribution:   Photon
BuildArch:      noarch

Source0: https://packages.vmware.com/photon/photon_sources/1.0/%{name}-%{version}-src.tar.gz
%define sha512 %{name}=fe59ad4867a00429719a7401701a433a90ed9c6ddb49a37072f8486ae0ca9c3da685a49d9376c8bb7b38f114a5293e1698b7fb314e71198bbb80f729547402eb

Patch0: use-system-provided-commons-httpclient-jar.patch

BuildRequires: openjdk8
BuildRequires: apache-ant
BuildRequires: commons-httpclient

Requires: apache-ant
Requires: (openjre8 or openjdk11-jre or openjdk17-jre)

%description
The Ant Contrib project is a collection of tasks for Apache Ant.

%prep
%autosetup -p1 -n %{name}

# Use system provided commons-httpclient jar instead of bundled one
find . -name '*.jar' -or -name '*.class' -exec rm -rf {} +
cp %{_datadir}/java/commons-httpclient/commons-httpclient.jar lib/commons-httpclient/jars/commons-httpclient-3.1.jar

%build
export JAVA_HOME=$(echo /usr/lib/jvm/OpenJDK-*)
ant \
    -Ddist.dir="." \
    -Dproject.version=%{version} \
    dist

%install
export JAVA_HOME=$(echo /usr/lib/jvm/OpenJDK-*)
mkdir -p -m 700 %{buildroot}%{_var}/opt
cd %{buildroot}%{_var}/opt
tar xzf %{_builddir}/%{name}/%{name}-%{version}-bin.tar.gz --wildcards "*.jar"

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{_prefix}
%dir %{_prefix}/lib
%{_prefix}/*.jar
%{_prefix}/lib/*.jar

%changelog
* Tue Mar 19 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.0b3-18
- Bump version as a part of openjdk8 upgrade
* Fri Sep 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0b3-17
- Require jre8 or jdk11-jre or jdk17-jre
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0b3-16
- Bump version as a part of openjdk8 upgrade
* Thu Nov 12 2020 Michelle Wang <michellew@vmware.com> 1.0b3-15
- Update Source0 use https://packages.vmware.com/photon/photon_sources
* Tue Oct 06 2020 Ankit Jain <ankitja@vmware.com> 1.0b3-14
- Use systems commons-httpclient
* Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 1.0b3-13
- Removed dependency on JAVA8_VERSION macro
* Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 1.0b3-12
- Removed dependency on ANT_HOME
* Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0b3-11
- Renamed openjdk to openjdk8
* Fri Apr 07 2017 Divya Thaluru <dthaluru@vmware.com> 1.0b3-10
- Removed prebuilt binaries from source tar ball
* Wed Dec 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0b3-9
- Updated JAVA_HOME path to point to latest.
* Tue Oct 04 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0b3-8
- Updated JAVA_HOME path to point to latest.
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0b3-7
- GA - Bump release of all rpms
* Fri May 20 2016 Divya Thaluru<dthaluru@vmware.com> 1.0b3-6
- Updated JAVA_HOME path to point to latest.
* Wed Mar 02 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0b3.0-5
- Updated apache-ant to version 1.9.6
* Fri Feb 26 2016 Kumar Kaushik <kaushikk@vmware.com> 1.0b3.0-4
- Updated JAVA_HOME path to point to latest.
* Mon Nov 16 2015 Sharath George <sharathg@vmware.com> 1.0b3.0-2
- Change path to /var/opt.
* Wed Sep 16 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.0b3.0-1
- Updated dependencies after repackaging openjdk.
* Tue Jun 9 2015 Sriram Nambakam <snambakam@vmware.com> 1.0b3.0-0
- Initial commit
