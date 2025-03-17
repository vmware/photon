%define network_required 1
Summary:          lightweight java application to send metrics to.
Name:             wavefront-proxy
Version:          13.4
Release:          3%{?dist}
URL:              https://github.com/wavefrontHQ/java
Group:            Development/Tools
Vendor:           VMware, Inc.
Distribution:     Photon

Source0: https://github.com/wavefrontHQ/wavefront-proxy/archive/refs/tags/proxy-%{version}.tar.gz

Source1:          %{name}.sysusers

Source2: license.txt
%include %{SOURCE2}

BuildRequires:    apache-maven
BuildRequires:    openjdk11
BuildRequires:    systemd-devel

Requires:         systemd
Requires:         (openjdk11-jre or openjdk17-jre)
Requires:         commons-daemon
Requires(pre):    systemd-rpm-macros
Requires(pre):    /usr/sbin/useradd /usr/sbin/groupadd

BuildArch:        noarch

%description
The Wavefront proxy is a light-weight Java application that you send your metrics to.
It handles authentication and the transmission of your metrics to your Wavefront instance.

%prep
%autosetup -p1 -n %{name}-proxy-%{version}

cat << EOF > %{name}.service
[Unit]
Description=The Wavefront Proxy Server
After=network.target

[Service]
PIDFile=/var/run/%{name}.pid
ExecStart=/usr/bin/java -Xmx4G -Xms1G -Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager -Dlog4j.configurationFile=/etc/wavefront/%{name}/log4j2.xml -jar "/opt/wavefront-push-agent.jar" -f /etc/wavefront/%{name}/wavefront.conf
ExecStop=/bin/kill -HUP \$MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sed -i 's/\/etc\/init.d\/$APP_BASE-proxy restart/ systemctl restart $APP_BASE-proxy/' \
        pkg/opt/wavefront/%{name}/bin/autoconf-%{name}.sh

sed -i 's/-jar \/opt\/wavefront\/%{name}\/bin\/wavefront-push-agent.jar/-jar \/opt\/wavefront-push-agent.jar/' \
        docker/run.sh

sed -i 's/InetAddress.getLocalHost().getHostName()/"localhost"/g' proxy/pom.xml

%build
export JAVA_HOME=$(echo %{_libdir}/jvm/OpenJDK*11.0*)
mvn -f proxy install -DskipTests -DskipFormatCode

%install
install -m 755 -D pkg/opt/wavefront/%{name}/bin/autoconf-%{name}.sh \
            %{buildroot}/opt/wavefront/%{name}/bin/autoconf-%{name}.sh

install -m 755 -D pkg/etc/wavefront/%{name}/log4j2-stdout.xml.default \
            %{buildroot}/%{_sysconfdir}/wavefront/%{name}/log4j2-stdout.xml

install -m 755 -D pkg/etc/wavefront/%{name}/log4j2.xml.default \
            %{buildroot}/%{_sysconfdir}/wavefront/%{name}/log4j2.xml

install -m 755 -D pkg/etc/wavefront/%{name}/preprocessor_rules.yaml.default \
            %{buildroot}/%{_sysconfdir}/wavefront/%{name}/preprocessor_rules.yaml

install -m 755 -D pkg/etc/wavefront/%{name}/wavefront.conf.default \
            %{buildroot}%{_sysconfdir}/wavefront/%{name}/wavefront.conf

install -m 755 -D pkg%{_docdir}/%{name}/copyright %{buildroot}%{_docdir}/%name/copyright

install -m 755 -D proxy/target/proxy-%{version}-spring-boot.jar \
            %{buildroot}/opt/wavefront-push-agent.jar

install -m 755 -D %{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -m 755 -D docker/run.sh %{buildroot}/opt/wavefront/%{name}/bin/run.sh
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%pre
user="wavefront"
group="wavefront"
%sysusers_create_compat %{SOURCE1}
spool_dir="/var/spool/%{name}"
log_dir="/var/log/wavefront"
[[ -d $spool_dir ]] || mkdir -p $spool_dir && chown $user:$group $spool_dir
[[ -d $log_dir ]] || mkdir -p $log_dir && chown $user:$group $log_dir

touch $log_dir/wavefront.log
chown $user:$group $log_dir/wavefront.log
chmod 644 $log_dir/wavefront.log

%post
chown -R wavefront:wavefront /opt/wavefront
chown -R wavefront:wavefront /etc/wavefront
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
/opt/*
%{_docdir}/*
%config(noreplace) %{_sysconfdir}/wavefront/%{name}/wavefront.conf
%{_sysconfdir}/wavefront/%{name}/log4j2-stdout.xml
%{_sysconfdir}/wavefront/%{name}/log4j2.xml
%{_sysconfdir}/wavefront/%{name}/preprocessor_rules.yaml
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.sysusers

%changelog
* Wed Jan 08 2025 Vamsi Krishna Brahmajosyula <vamsi-krishna.brahmajosyula@broadcom.com> 13.4-3
- Release bump for network_required packages
* Wed Dec 11 2024 Keerthana K <keerthana.kalyanasundaram@broadcom.com> 13.4-2
- Release bump for SRP compliance
* Fri Nov 10 2023 Prashant S Chauhan <psinghchauha@vmware.com> 13.4-1
- Update to 13.4
* Sat Aug 26 2023 Shreenidhi Shedi <sshedi@vmware.com> 13.0-3
- Require jdk11 or jdk17
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 13.0-2
- Resolving systemd-rpm-macros for group creation
* Mon Jul 31 2023 Prashant S Chauhan <psinghchauha@vmware.com> 13.0-1
- Update to 13.0
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 12.1-4
- Bump version as a part of openjdk11 upgrade
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 12.1-3
- Use systemd-rpm-macros for user creation
* Fri Mar 03 2023 Srish Srinivasan <ssrish@vmware.com> 12.1-2
- bump release as part of apache-maven update
* Mon Oct 24 2022 Prashant S Chauhan <psinghchauha@vmware.com> 12.1-1
- Update to version 12.1
* Wed Sep 21 2022 Vamsi Krishna Brahmajosuyula <vbrahmajosyula@vmware.com> 11.0-2
- Use openjdk11
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 11.0-1
- Automatic Version Bump
* Wed Jun 10 2020 Gerrit Photon <photon-checkins@vmware.com> 9.2-1
- Automatic Version Bump
* Tue Jan 21 2020 Ankit Jain <ankitja@vmware.com> 4.39-2
- Upgraded net.openhft chronicle-map version
* Mon Jul 29 2019 Shreyas B. <shreyasb@vmware.com> 4.39-1
- Updated to 4.39
* Wed Jul 10 2019 Alexey Makhalov <amakhalov@vmware.com> 4.32-2
- Skip tests during make install.
* Thu Dec 06 2018 Ankit Jain <ankitja@vmware.com> 4.32-1
- updated to 4.32
* Tue Nov 20 2018 Ajay Kaher <akaher@vmware.com> 4.28-4
- Fix for aarch64
* Wed Oct 24 2018 Ajay Kaher <akaher@vmware.com> 4.28-3
- Adding BuildArch
* Wed Oct 24 2018 Srivatsa S. Bhat (VMware) <srivatsa@csail.mit.edu> 4.28-2
- Reduce memory needed for service to 1GB.
* Tue Sep 04 2018 Ankit Jain <ankitja@vmware.com> 4.28-1
- Updated to latest version 4.28
* Mon Oct 09 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.16-4
- Add Docker related files to the package
* Tue Oct 03 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.16-3
- Fix for CVE-2017-9735
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 4.16-2
- Remove shadow from requires and use explicit tools for post actions
* Tue Jul 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 4.16-1
- first version.
