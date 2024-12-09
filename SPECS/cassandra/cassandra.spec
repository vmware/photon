%define network_required 1
%global debug_package %{nil}
%global __os_install_post %{nil}

Summary:        Cassandra is a highly scalable, eventually consistent, distributed, structured key-value store
Name:           cassandra
Version:        4.0.10
Release:        6%{?dist}
URL:            http://cassandra.apache.org/
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://archive.apache.org/dist/cassandra/%{version}/apache-%{name}-%{version}-src.tar.gz
%define sha512 apache-%{name}=986b79556e5d375ee6f385919509555bb79a6ae3c3dd338003ca8bb2145d2311a170eee17e98025f08b61b0ea0bc3712da696207644c6db05f15d0ec54c1022a

Source1:        %{name}.service
Source2:        %{name}.sysusers
Source3:        %{name}-%{version}-dependencies.tar.gz
%define sha512  %{name}-%{version}-dependencies.tar.gz=3532aea87265980716d0f920376b135f65e1729bc8a101ad7aa4088d1477948c4897e8b1a0687bacbb5af50315069245da7bafa8ec2b2da7ae637d5e07f8057a

Source4: license.txt
%include %{SOURCE4}

BuildRequires:  apache-ant
BuildRequires:  unzip
BuildRequires:  zip
BuildRequires:  openjdk11
BuildRequires:  wget
BuildRequires:  git
BuildRequires:  systemd-devel

Requires:       openjdk11-jre
Requires:       gawk
Requires:       shadow
Requires(pre): systemd-rpm-macros
Requires(post): /usr/bin/chown
%{?systemd_requires}

%description
Cassandra is a highly scalable, eventually consistent, distributed, structured key-value store.
Cassandra brings together the distributed systems technologies from Dynamo and the log-structured storage engine from Google's BigTable.

%prep
%autosetup -p1 -n apache-%{name}-%{version}-src
mkdir -p $HOME/.m2/repository/org/
tar xf %{SOURCE3} -C $HOME/.m2/repository/org/

%build
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK-*)

if [ -n "${MAVEN_PROXY_URL}" ]; then
  PROP_FILE="build.properties.default"
  if grep -q "https://repo1.maven.org/maven2" "$PROP_FILE" && grep -q "https://repo.maven.apache.org/maven2" "$PROP_FILE"; then
      sed -i "s|https://repo1.maven.org/maven2|${MAVEN_PROXY_URL}/|" "$PROP_FILE"
      sed -i "s|https://repo.maven.apache.org/maven2|${MAVEN_PROXY_URL}/|" "$PROP_FILE"
  else
      echo "One or both URLs not found in the property file."
      exit 1
  fi
fi

ant jar javadoc -Drelease=true -Duse.jdk11=true
#Remove libraries of other arch
%ifarch x86_64
rm $(find lib/sigar-bin -type f -name "*" ! -name "libsigar-amd64-linux.so")
%endif
%ifarch aarch64
rm -r lib/sigar-bin
%endif

%install
mkdir -p %{buildroot}%{_localstatedir}/opt/%{name}/data \
         %{buildroot}%{_localstatedir}/log/%{name} \
         %{buildroot}%{_bindir} \
         %{buildroot}%{_sbindir} \
         %{buildroot}%{_datadir}/%{name} \
         %{buildroot}%{_sysconfdir}/%{name} \
         %{buildroot}%{_sysconfdir}/sysconfig \
         %{buildroot}%{_sysconfdir}/profile.d \
         %{buildroot}%{_unitdir}

cp -pr conf/* %{buildroot}%{_sysconfdir}/%{name}

rm -f bin/cqlsh bin/cqlsh.py
mv bin/%{name} %{buildroot}%{_sbindir}
mv bin/%{name}.in.sh %{buildroot}%{_datadir}/%{name}/
cp -p bin/* tools/bin/* %{buildroot}%{_bindir}/
cp -r lib build %{buildroot}%{_localstatedir}/opt/%{name}/

cp -p build/tools/lib/stress.jar build/apache-%{name}-%{version}.jar %{buildroot}%{_localstatedir}/opt/%{name}/lib

install -p -D -m 644 %{SOURCE1}  %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.sysusers

cat >> %{buildroot}%{_sysconfdir}/sysconfig/%{name} <<- "EOF"
CASSANDRA_HOME=%{_localstatedir}/opt/%{name}/
CASSANDRA_CONF=%{_sysconfdir}/%{name}/
EOF

cat >> %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh <<- "EOF"
export CASSANDRA_HOME=%{_localstatedir}/opt/%{name}/
export CASSANDRA_CONF=%{_sysconfdir}/%{name}/
EOF

%pre
%sysusers_create_compat %{SOURCE2}

%post
%{_sbindir}/ldconfig
chown -R %{name}: %{_localstatedir}/opt/%{name}
source %{_sysconfdir}/profile.d/%{name}.sh
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%{_sbindir}/ldconfig
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%doc README.asc CHANGES.txt NEWS.txt conf/cqlshrc.sample LICENSE.txt NOTICE.txt
%dir %{_localstatedir}/opt/%{name}
%{_bindir}/*
%{_datadir}/%{name}
%{_localstatedir}/opt/%{name}
%{_sbindir}
%{_sysconfdir}/%{name}
%{_sysconfdir}/sysconfig/%{name}
%{_sysconfdir}/profile.d/%{name}.sh
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.sysusers
%exclude %{_localstatedir}/opt/%{name}/build/lib

%changelog
* Thu Dec 12 2024 HarinadhD <harinadh.dommaraju@broadcom.com> 4.0.10-6
- Release bump for SRP compliance
* Wed Jul 24 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 4.0.10-5
- Add changes to build offline cassandra
* Sat Aug 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.0.10-4
- Require jdk11
- cassandra doesn't work with jdk17 yet
- https://issues.apache.org/jira/browse/CASSANDRA-16895
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 4.0.10-3
- Resolving systemd-rpm-macros for group creation
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 4.0.10-2
- Bump version as a part of openjdk11 upgrade
* Fri Jun 02 2023 Ankit Jain <ankitja@vmware.com> 4.0.10-1
- Updated to v4.0.10.
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 4.0.8-2
- Use systemd-rpm-macros for user creation
* Tue Feb 21 2023 Ankit Jain <ankitja@vmware.com> 4.0.8-1
- Updated to v4.0.8. This version added support for python-3.11
* Mon Oct 31 2022 Gerrit Photon <photon-checkins@vmware.com> 4.0.7-1
- Automatic Version Bump
* Fri Oct 07 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 4.0.6-1
- Use openjdk11
- Upgrade to 4.0.6
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 4.0.4-1
- Automatic Version Bump
* Sun May 29 2022 Shreenidhi Shedi <sshedi@vmware.com> 4.0.3-2
- Fix binary path
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 4.0.3-1
- Automatic Version Bump
* Thu Nov 11 2021 Shreenidhi Shedi <sshedi@vmware.com> 4.0.1-1
- Update to 4.0.1
* Wed Jun 09 2021 Ankit Jain <ankitja@vmware.com> 3.11.10-2
- Remove cqlsh and cqlsh.py, since it requires python2 to run
- python3-cqlsh is introduced
- fix post and postun script failure
* Tue Mar 09 2021 Ankit Jain <ankitja@vmware.com> 3.11.10-1
- Update to 3.11.10 to fix CVE-2020-17516
* Thu Oct 29 2020 Ankit Jain <ankitja@vmware.com> 3.11.8-2
- Added cqlsh and cqlsh.py.
- Since, python-cqlsh is deprecated.
* Tue Sep 01 2020 Gerrit Photon <photon-checkins@vmware.com> 3.11.8-1
- Automatic Version Bump
* Mon Aug 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.11.7-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 3.11.6-1
- Automatic Version Bump
* Wed Feb 05 2020 Ankit Jain <ankitja@vmware.com> 3.11.5-3
- Bump jackson version to >= 2.9.5
* Wed Feb 05 2020 Shreyas B. <shreyasb@vmware.com> 3.11.5-2
- Shadow require by Cassandra for the installation.
* Fri Jan 17 2020 Ankit Jain <ankitja@vmware.com> 3.11.5-1
- Central maven repository not responding, Updated to 3.11.5
* Tue Dec 17 2019 Shreyas B. <shreyasb@vmware.com> 3.11.3-3
- Bumping up the thrift version to 0.9.3.1 to fix vulnerability.
* Mon Nov 05 2018 Alexey Makhalov <amakhalov@vmware.com> 3.11.3-2
- Removed dependency on JAVA8_VERSION macro
* Mon Sep 03 2018 Keerthana K <keerthanak@vmware.com> 3.11.3-1
- Updated to version 3.11.3.
* Tue Apr 24 2018 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-8
- Remove patch to build on openjdk-1.8.0.162, updated openjdk to 1.8.0.172
* Sat Jan 20 2018 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-7
- Add patch to build on openjdk-1.8.0.162
* Thu Aug 17 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-6
- Add SuccessExitStatus to cassandra service file
* Thu Aug 10 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-5
- Remove the build/libs directory from the cassandra package
* Tue Jul 25 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-4
- Remove hadoop jars, upgrade logback jars and change service type to simple
* Mon Jul 10 2017 Xiaolin Li <xiaolinl@vmware.com> 3.10-3
- Remove cqlsh and cqlsh.py.
* Mon Jun 19 2017 Divya Thaluru <dthaluru@vmware.com> 3.10-2
- Removed dependency on ANT_HOME
* Mon May 08 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.10-1
- Initial build. First version
