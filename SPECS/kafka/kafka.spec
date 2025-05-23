%define network_required 1
%define debug_package %{nil}
%define _conf_dir     %{_sysconfdir}/%{name}
%define _log_dir      %{_var}/log/%{name}
%define _data_dir     %{_sharedstatedir}/%{name}

Summary:       Apache Kafka is publish-subscribe messaging rethought as a distributed commit log.
Name:          kafka
Version:       3.4.0
Release:       10%{?dist}
Group:         Productivity/Networking/Other
URL:           http://kafka.apache.org/
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: %{name}-%{version}-src.tgz

Source1:       %{name}.service
Source2:       %{name}.sysusers

#Download https://raw.githubusercontent.com/gradle/gradle/v7.6.0/gradle/wrapper/gradle-wrapper.jar
Source3:       gradle-wrapper-7.6.0-jar.tar.gz

Source4: license.txt
%include %{SOURCE4}

Patch0:     0001-Use-proxy-if-available.patch
Patch1:     kafka_doc.patch

Provides:   kafka
Provides:   kafka-server

BuildRequires: systemd-devel
BuildRequires: curl
BuildRequires: zookeeper
BuildRequires: openjdk11

Requires: zookeeper
Requires: systemd-rpm-macros
Requires: (openjdk11-jre or openjdk17-jre)

%{?systemd_requires}

%description
Kafka is designed to allow a single cluster to serve as the central data backbone for a large organization.
It can be elastically and transparently expanded without downtime.
Data streams are partitioned and spread over a cluster of machines to allow data streams larger than the capability of any single machine and to allow clusters of co-ordinated consumers.
Messages are persisted on disk and replicated within the cluster to prevent data loss.

%prep
%autosetup -p1 -n %{name}-%{version}-src -a3

%build
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK*)
# Use system proxy (if enabled) for gradle
JAVA_HTTP_PROXY_OPTS="$(echo "$HTTP_PROXY" | sed -ne 's|^http://\(.*\):\(.*\)|-Dhttp.proxyHost=\1 -Dhttp.proxyPort=\2|p')"
JAVA_HTTPS_PROXY_OPTS="$(echo "$HTTPS_PROXY" | sed -ne 's|^http://\(.*\):\(.*\)|-Dhttps.proxyHost=\1 -Dhttps.proxyPort=\2|p')"
export GRADLE_OPTS="$JAVA_HTTP_PROXY_OPTS $JAVA_HTTPS_PROXY_OPTS"

cp gradle-wrapper.jar gradle/wrapper/

if [ -n "${GRADLE_PROXY_URL}" ]; then
  PROP_FILE="gradle/wrapper/gradle-wrapper.properties"
  sed -i "s|\(distributionUrl=\).*/\(gradle-.*.zip\)|\1${GRADLE_DISTRIBUTION_URL}/\2|" "$PROP_FILE"
fi

./gradlew jar
./gradlew srcJar
./gradlew javadoc
./gradlew javadocJar
./gradlew scaladoc
./gradlew scaladocJar
./gradlew docsJar

%install
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK*)

mkdir -p %{buildroot}/%{_prefix}/%{name}/{libs,bin,config} \
         %{buildroot}/%{_log_dir} \
         %{buildroot}/%{_data_dir} \
         %{buildroot}/%{_unitdir} \
         %{buildroot}/%{_conf_dir}/

cp -pr config/* %{buildroot}/%{_prefix}/%{name}/config
install -p -D -m 755 bin/*.sh %{buildroot}/%{_prefix}/%{name}/bin
install -p -D -m 644 config/server.properties %{buildroot}/%{_conf_dir}/
install -p -D -m 644 config/zookeeper.properties %{buildroot}/%{_conf_dir}/
install -p -D -m 755 %{S:1} %{buildroot}/%{_unitdir}/
install -p -D -m 644 config/log4j.properties %{buildroot}/%{_conf_dir}/
install -p -D -m 644 connect/mirror/build/dependant-libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 connect/runtime/build/dependant-libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 tools/build/dependant-libs-2.13.10/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 core/build/dependant-libs-2.13.10/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 core/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 clients/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 connect/api/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 connect/basic-auth-extension/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 connect/json/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 connect/transforms/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 connect/file/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 connect/mirror-client/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 streams/examples/build/dependant-libs-2.13.10/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 streams/upgrade-system-tests-0100/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 644 streams/build/libs/* %{buildroot}/%{_prefix}/%{name}/libs
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf

%clean
rm -rf %{buildroot}

%pre
%sysusers_create_compat %{SOURCE2}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root)
%{_unitdir}/%{name}.service
%config(noreplace) %{_conf_dir}/*
%{_prefix}/%{name}
%attr(0755,kafka,kafka) %dir %{_log_dir}
%attr(0700,kafka,kafka) %dir %{_data_dir}
%{_sysusersdir}/%{name}.conf
%doc NOTICE
%doc LICENSE

%changelog
* Thu May 08 2025 Mukul Sikka <mukul.sikka@broadcom.com> 3.4.0-10
- Renaming sysusers to conf to fix auto user creation
* Fri Jan 10 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.4.0-9
- Add support for reporting gradle plugin inputs to SRP.
* Wed Jan 08 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.4.0-8
- Release bump for network_required packages
* Wed Dec 11 2024 Tapas Kundu <tapas.kundu@broadcom.com> 3.4.0-7
- Release bump for SRP compliance
* Wed Sep 04 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.4.0-6
- Removed javadoc oracle links
* Tue Jul 16 2024 Shivani Agarwal <shivani.agarwal@broadcom.com> 3.4.0-5
- Use proxy if available
* Sat Aug 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.4.0-4
- Require jdk11 or jdk17
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 3.4.0-3
- Resolving systemd-rpm-macros for group creation
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 3.4.0-2
- Bump version as a part of openjdk11 upgrade
* Fri May 19 2023 Prashant S Chauhan <psinghchauha@vmware.com> 3.4.0-1
- Update to 3.4.0, Fixes CVE-2023-25194
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 3.3.1-2
- Use systemd-rpm-macros for user creation
* Tue Nov 1 2022 Gerrit Photon <photon-checkins@vmware.com> 3.3.1-1
- Automatic Version Bump
* Wed Sep 28 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2.3-1
- Automatic Version Bump
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 3.2.0-2
- Use openjdk11
* Thu May 19 2022 Gerrit Photon <photon-checkins@vmware.com> 3.2.0-1
- Automatic Version Bump
* Fri Jul 31 2020 Anisha Kumari <kanisha@vmware.com> 2.5.0-1
- initial package
