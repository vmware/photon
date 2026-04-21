%global build_if %{photon_subrelease} <= 91

%define network_required 1
%define debug_package %{nil}
%define _conf_dir     %{_sysconfdir}/%{name}
%define _log_dir      %{_var}/log/%{name}
%define _data_dir     %{_sharedstatedir}/%{name}
%define _lib_dir      %{_prefix}/%{name}/libs
%define _scalaver     2.13
%define dep_libs_ver  %{_scalaver}.15

Summary:       Apache Kafka is publish-subscribe messaging rethought as a distributed commit log.
Name:          kafka
Version:       3.9.1
Release:       7.1%{?dist}
Group:         Productivity/Networking/Other
URL:           http://kafka.apache.org/
Vendor:        VMware, Inc.
Distribution:  Photon

Source0: %{name}-%{version}-src.tgz

Source1:       %{name}.service
Source2:       %{name}.sysusers

Source3: license.txt
%include %{SOURCE3}

#Download https://raw.githubusercontent.com/gradle/gradle/v8.10.2/gradle/wrapper/gradle-wrapper.jar
Source4:       gradle-wrapper-8.10.2-jar.tar.gz

Patch0:     0001-Use-proxy-if-available.patch
Patch1:     CVE-2024-29371-bump-jose4j.patch

Provides:   kafka
Provides:   kafka-server

BuildRequires: systemd-devel
BuildRequires: systemd-rpm-macros
BuildRequires: curl
BuildRequires: zookeeper
BuildRequires: openjdk11

Requires: zookeeper
Requires: systemd-rpm-macros
Requires: jre >= 11.0
Requires(pre): shadow
Requires(post): (coreutils or coreutils-selinux)

%{?systemd_requires}

%description
Kafka is designed to allow a single cluster to serve as the central data backbone for a large organization.
It can be elastically and transparently expanded without downtime.
Data streams are partitioned and spread over a cluster of machines to allow data streams larger than the capability of any single machine and to allow clusters of co-ordinated consumers.
Messages are persisted on disk and replicated within the cluster to prevent data loss.

%prep
%autosetup -p1 -n %{name}-%{version}-src -a4

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

./gradlew --no-daemon compileJava compileScala releaseTargz

%install
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK*)

mkdir -p %{buildroot}/%{_prefix}/%{name}/{libs,bin,config} \
         %{buildroot}/%{_log_dir} \
         %{buildroot}/%{_data_dir} \
         %{buildroot}/%{_unitdir} \
         %{buildroot}/%{_conf_dir}/

mkdir dist
tar -xf "core/build/distributions/%{name}_%{_scalaver}-%{version}.tgz" --strip 1 -C "dist"

cp -pr dist/config/* %{buildroot}/%{_prefix}/%{name}/config

install -p -D -m 644 dist/config/server.properties %{buildroot}/%{_conf_dir}/
install -p -D -m 644 dist/config/zookeeper.properties %{buildroot}/%{_conf_dir}/
install -p -D -m 644 dist/config/log4j.properties %{buildroot}/%{_conf_dir}/
install -p -D -m 755 dist/bin/*.sh %{buildroot}/%{_prefix}/%{name}/bin
install -p -D -m 755 dist/libs/* %{buildroot}%{_lib_dir}
install -p -D -m 755 %{S:1} %{buildroot}/%{_unitdir}/
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysusersdir}/%{name}.conf

cat << EOF >> %{buildroot}/%{_conf_dir}/%{name}.env
LOG_DIR=/var/log/kafka
EOF

%clean
rm -rf %{buildroot}

%pre
%sysusers_create_compat %{SOURCE2}

%post
if [ -d %{_prefix}/%{name}/logs ] && [ ! -L %{_prefix}/%{name}/logs ]; then
    shopt -s dotglob
    mv %{_prefix}/%{name}/logs/* %{_log_dir}/
    shopt -u dotglob
    rmdir %{_prefix}/%{name}/logs/
    ln -s %{_log_dir} %{_prefix}/%{name}/logs
fi
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root)
%{_unitdir}/%{name}.service
%config(noreplace) %{_conf_dir}/*
%attr(0755,kafka,kafka) %{_prefix}/%{name}
%attr(0755,kafka,kafka) %dir %{_log_dir}
%attr(0700,kafka,kafka) %dir %{_data_dir}
%{_sysusersdir}/%{name}.conf
%doc NOTICE
%doc LICENSE

%changelog
* Tue Apr 21 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 3.9.1-7.1
- Bump after moving to SPECS/91
* Fri Apr 03 2026 Harinadh Dommaraju <Harinadh.Dommaraju@broadcom.com> 3.9.1-7
- Fixes CVE-2024-29371,bump jose4j to 0.9.6
* Tue Feb 24 2026 Oliver Kurth <oliver.kurth@broadcom.com> 3.9.1-6
- Add missing shadow dependency for user creation
* Fri Aug 15 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 3.9.1-5
- Update Requires to jre >= 11.0
* Mon Aug 11 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.9.1-4
- Add gradle-wrapper.jar tar for SRP compliance
* Thu Jul 24 2025 Prashant S Chauha <prashant.singh-chauhan@broadcom.com> 3.9.1-3
- Package additional missing jar files
* Wed Jul 09 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.9.1-2
- Release bump up for SRP compliance
* Thu May 15 2025 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 3.9.1-1
- Update to 3.9.1, fixes multiple CVEs
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
