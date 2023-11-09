Summary:        lightweight java application to send metrics to.
Name:           wavefront-proxy
Version:        13.4
Release:        1%{?dist}
License:        Apache 2.0
URL:            https://github.com/wavefrontHQ/java
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/wavefrontHQ/wavefront-proxy/archive/refs/tags/proxy-%{version}.tar.gz
%define sha512  proxy=66f3fc224d6fc199de1a3928e84c21323c2a9ef38d3dac1e4b6b7148d64dabd6ccae870ac4d1c9effb9a0d1c47c35f9d154418e277893a2f0d15e8ed9845f41f
BuildRequires:  apache-maven
BuildRequires:  openjdk11
BuildRequires:  systemd-devel

Requires:       systemd
Requires:       openjdk11
Requires:       commons-daemon
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel

BuildArch:      noarch

%description
The Wavefront proxy is a light-weight Java application that you send your metrics to.
It handles authentication and the transmission of your metrics to your Wavefront instance.

%prep
%autosetup -p1 -n %{name}-proxy-%{version}

cat << EOF >> %{name}.service
[Unit]
Description=The Wavefront Proxy Server
After=network.target

[Service]
PIDFile=%{_var}/run/%{name}.pid
ExecStart=%{_bindir}/java -Xmx4G -Xms1G -Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager -Dlog4j.configurationFile=%{_sysconfdir}/wavefront/%{name}/log4j2.xml -jar "/opt/wavefront-push-agent.jar" -f %{_sysconfdir}/wavefront/%{name}/wavefront.conf
ExecStop=%{_bindir}/kill -HUP \$MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
sed -i 's/\/etc\/init.d\/$APP_BASE-proxy restart/ systemctl restart $APP_BASE-proxy/' pkg/opt/wavefront/%{name}/bin/autoconf-%{name}.sh
sed -i 's/-jar \/opt\/wavefront\/%{name}\/bin\/wavefront-push-agent.jar/-jar \/opt\/wavefront-push-agent.jar/' docker/run.sh
sed -i 's/InetAddress.getLocalHost().getHostName()/"localhost"/g' proxy/pom.xml

%build
export JAVA_HOME=$(echo /usr/lib/jvm/OpenJDK*11.0*)
mvn -f proxy install -DskipTests -DskipFormatCode

%install
install -m 755 -D pkg/opt/wavefront/%{name}/bin/autoconf-%{name}.sh %{buildroot}/opt/wavefront/%{name}/bin/autoconf-%{name}.sh
install -m 755 -D pkg/etc/wavefront/%{name}/log4j2-stdout.xml.default %{buildroot}/%{_sysconfdir}/wavefront/%{name}/log4j2-stdout.xml
install -m 755 -D pkg/etc/wavefront/%{name}/log4j2.xml.default %{buildroot}/%{_sysconfdir}/wavefront/%{name}/log4j2.xml
install -m 755 -D pkg/etc/wavefront/%{name}/preprocessor_rules.yaml.default %{buildroot}/%{_sysconfdir}/wavefront/%{name}/preprocessor_rules.yaml
install -m 755 -D pkg/etc/wavefront/%{name}/wavefront.conf.default %{buildroot}%{_sysconfdir}/wavefront/%{name}/wavefront.conf
install -m 755 -D pkg%{_docdir}/%{name}/copyright %{buildroot}%{_docdir}/%name/copyright
install -m 755 -D proxy/target/proxy-%{version}-spring-boot.jar %{buildroot}/opt/wavefront-push-agent.jar
install -m 755 -D %{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -m 755 -D docker/run.sh %{buildroot}/opt/wavefront/%{name}/bin/run.sh

%pre
user="wavefront"
group="wavefront"
getent group $group >/dev/null || groupadd -r $group
getent passwd $user >/dev/null || useradd -c "Wavefront Proxy Server" -d /opt/wavefront -g $group \
        -s /sbin/nologin -M -r $user
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
if [ $1 -eq 0 ] ; then
    getent passwd wavefront >/dev/null && userdel wavefront
    getent group wavefront >/dev/null && groupdel wavefront
fi
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

%changelog
* Fri Nov 10 2023 Prashant S Chauhan <psinghchauha@vmware.com> 13.4-1
- Update to 13.4
* Mon Jul 31 2023 Prashant S Chauhan <psinghchauha@vmware.com> 13.0-1
- Update to 13.0
* Sat Jun 17 2023 Shreenidhi Shedi <sshedi@vmware.com> 12.4-2
- Bump version as a part of openjdk11 upgrade
* Mon Jun 05 2023 Prashant S Chauhan <psinghchauha@vmware.com> 12.4-1
- Update to 12.4
* Fri Dec 16 2022 Prashant S Chauhan <psinghchauha@vmware.com> 12.1-1
- Update to version 12.1
* Mon Oct 24 2022 Prashant S Chauhan <psinghchauha@vmware.com> 11.4-1
- Update to version 11.4
* Tue May 24 2022 Prashant S Chauhan <psinghchauha@vmware.com> 11.3-1
- Use openjdk11 to build wavefront-proxy, Update to 11.3
* Mon May 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 11.1-2
- Bump version as a part of apache-maven upgrade
* Fri May 20 2022 Prashant S Chauhan <psinghchauha@vmware.com> 11.1-1
- Upgrade to 11.1
* Thu Mar 10 2022 Piyush Gupta <gpiyush@vmware.com> 10.14-1
- Upgrade to 10.14.
* Tue Dec 14 2021 Dweep Advani <dadvani@vmware.com> 9.7-2
- Fixed for CVE-2021-44228 in log4j by consuming version 2.16.0
* Fri Jun 04 2021 Prashant S Chauhan <psinghchauha@vmware.com> 9.7-1
- Update version to 9.7
* Wed Aug 26 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 4.39-3
- Fix app check scan vulnerabilities
* Tue Jan 21 2020 Ankit Jain <ankitja@vmware.com> 4.39-2
- Upgraded net.openhft chronicle-map version
* Mon Jul 29 2019 Shreyas B. <shreyasb@vmware.com> 4.39-1
- Updated to 4.39
* Fri Jul 12 2019 Sujay G <gsujay@vmware.com> 4.36-2
- Skip tests during build.
* Thu Mar 14 2019 Keerthana K <keerthanak@vmware.com> 4.36-1
- Updated to 4.36
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
- first version
