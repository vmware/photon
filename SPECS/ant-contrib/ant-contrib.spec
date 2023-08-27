%define ant_prefix %{_var}/opt/ant-contrib

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
Patch1: ant-contrib-java-8.patch

BuildRequires: openjdk11
BuildRequires: apache-ant
BuildRequires: commons-httpclient

Requires: (openjdk11-jre or openjdk17-jre)
Requires: apache-ant

%description
The Ant Contrib project is a collection of tasks for Apache Ant.

%prep
%autosetup -p1 -n %{name}
# Use system provided commons-httpclient jar instead of bundled one
find . -name '*.jar' -or -name '*.class' -delete

cp %{_datadir}/java/commons-httpclient/commons-httpclient.jar \
       lib/commons-httpclient/jars/commons-httpclient-3.1.jar

%build
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK-*)
ant -Ddist.dir="." -Dproject.version=%{version} dist

%install
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK-*)
mkdir -p -m 700 %{buildroot}%{_var}/opt

cd %{buildroot}%{_var}/opt
tar xzf %{_builddir}/%{name}/%{name}-%{version}-bin.tar.gz --wildcards "*.jar"

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir %{ant_prefix}
%dir %{ant_prefix}/lib
%{ant_prefix}/*.jar
%{ant_prefix}/lib/*.jar

%changelog
* Sat Aug 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0b3-18
- Require jdk11 or jdk17
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.0b3-17
- Bump version as a part of openjdk11 upgrade
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 1.0b3-16
- Use openjdk11
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
