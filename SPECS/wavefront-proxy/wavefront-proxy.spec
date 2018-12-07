Summary:        lightweight java application to send metrics to.
Name:           wavefront-proxy
Version:        4.32
Release:        1%{?dist}
License:        Apache 2.0
URL:            https://github.com/wavefrontHQ/java
Source0:        https://github.com/wavefrontHQ/java/archive/wavefront-%{version}.tar.gz
%define sha1    wavefront=216c16125c6308debcffc1d6bd3969b9ea5013eb
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon
BuildRequires:  apache-maven
BuildRequires:  openjre8
BuildRequires:  openjdk8
BuildRequires:  systemd-devel
Requires:       systemd
Requires:       openjre8
Requires:       commons-daemon
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd
Requires(postun):/usr/sbin/userdel /usr/sbin/groupdel
BuildArch:      noarch

%description
The Wavefront proxy is a light-weight Java application that you send your metrics to.
It handles authentication and the transmission of your metrics to your Wavefront instance.

%prep
%setup -n java-wavefront-%{version}

cat << EOF >>wavefront-proxy.service
[Unit]
Description=The Wavefront Proxy Server
After=network.target

[Service]
PIDFile=/var/run/wavefront-proxy.pid
ExecStart=/usr/bin/java -Xmx4G -Xms1G -Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager -Dlog4j.configurationFile=/etc/wavefront/wavefront-proxy/log4j2.xml -jar "/opt/wavefront-push-agent.jar" -f /etc/wavefront/wavefront-proxy/wavefront.conf
ExecStop=/bin/kill -HUP \$MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
sed -i 's/\/etc\/init.d\/$APP_BASE-proxy restart/ systemctl restart $APP_BASE-proxy/' pkg/opt/wavefront/wavefront-proxy/bin/autoconf-wavefront-proxy.sh
sed -i 's/-jar \/opt\/wavefront\/wavefront-proxy\/bin\/wavefront-push-agent.jar/-jar \/opt\/wavefront-push-agent.jar/' proxy/docker/run.sh

%build
%if "%{_arch}" == "aarch64"
mvn install -DskipTests
%else
mvn install
%endif

%install
install -m 755 -D pkg/opt/wavefront/wavefront-proxy/bin/autoconf-wavefront-proxy.sh %{buildroot}/opt/wavefront/%{name}/bin/autoconf-wavefront-proxy.sh
install -m 755 -D pkg/etc/wavefront/wavefront-proxy/log4j2-stdout.xml.default %{buildroot}/%{_sysconfdir}/wavefront/%{name}/log4j2-stdout.xml
install -m 755 -D pkg/etc/wavefront/wavefront-proxy/log4j2.xml.default %{buildroot}/%{_sysconfdir}/wavefront/%{name}/log4j2.xml
install -m 755 -D pkg/etc/wavefront/wavefront-proxy/preprocessor_rules.yaml.default %{buildroot}/%{_sysconfdir}/wavefront/%{name}/preprocessor_rules.yaml
install -m 755 -D pkg/etc/wavefront/wavefront-proxy/wavefront.conf.default %{buildroot}/%{_sysconfdir}/wavefront/%{name}/wavefront.conf
install -m 755 -D pkg/usr/share/doc/wavefront-proxy/copyright %{buildroot}/%{_docdir}/%name/copyright
install -m 755 -D proxy/target/proxy-%{version}-uber.jar %{buildroot}/opt/wavefront-push-agent.jar
install -m 755 -D wavefront-proxy.service %{buildroot}/%{_unitdir}/wavefront-proxy.service
install -m 755 -D proxy/docker/run.sh %{buildroot}/opt/wavefront/%{name}/bin/run.sh

%pre
user="wavefront"
group="wavefront"
getent group $group >/dev/null || groupadd -r $group
getent passwd $user >/dev/null || useradd -c "Wavefront Proxy Server" -d /opt/wavefront -g $group \
        -s /sbin/nologin -M -r $user
spool_dir="/var/spool/wavefront-proxy"
log_dir="/var/log/wavefront"
[[ -d $spool_dir ]] || mkdir -p $spool_dir && chown $user:$group $spool_dir
[[ -d $log_dir ]] || mkdir -p $log_dir && chown $user:$group $log_dir

touch $log_dir/wavefront-daemon.log
touch $log_dir/wavefront-error.log
chown $user:$group $log_dir/wavefront-daemon.log
chown $user:$group $log_dir/wavefront-error.log
chmod 644 $log_dir/wavefront-daemon.log
chmod 644 $log_dir/wavefront-error.log

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

rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
/opt/*
%{_docdir}/*
%config(noreplace) %{_sysconfdir}/wavefront/%{name}/wavefront.conf
%{_sysconfdir}/wavefront/%{name}/log4j2-stdout.xml
%{_sysconfdir}/wavefront/%{name}/log4j2.xml
%{_sysconfdir}/wavefront/%{name}/preprocessor_rules.yaml
%{_unitdir}/wavefront-proxy.service

%changelog
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
