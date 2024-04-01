Summary:        Application Container Server for Networked/Clustered Web Applications
Name:           uwsgi
Version:        2.0.21
Release:        17%{?dist}
License:        GPLv2 with exceptions
Group:          Productivity/Networking/Web/Servers
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/unbit/uwsgi

Source0: http://projects.unbit.it/downloads/%{name}-%{version}.tar.gz
%define sha512 %{name}=36a9c1b87a4c3d08482b9045d2227f56b006acb53f38ddf1b510880ae5fc24c0177a077338ec8af3ef0b8f8e220bc4fc7f8311dab8066e13cbcbb616f736c795

Source1: photon.ini
Source2: %{name}.service
Source3: %{name}.ini
Source4: %{name}.sysusers

BuildRequires: python3-devel
BuildRequires: jansson-devel
BuildRequires: libxml2-devel
BuildRequires: curl-devel
BuildRequires: libyaml-devel
BuildRequires: libedit-devel
BuildRequires: krb5-devel
BuildRequires: openssl-devel
BuildRequires: bzip2-devel
BuildRequires: gmp-devel
BuildRequires: Linux-PAM-devel
BuildRequires: sqlite-devel
BuildRequires: libcap-devel
BuildRequires: httpd-devel
BuildRequires: curl-libs
BuildRequires: libstdc++-devel
BuildRequires: openldap-devel
BuildRequires: boost-devel
BuildRequires: attr-devel
BuildRequires: libxslt-devel
BuildRequires: systemd-devel
BuildRequires: tcp_wrappers-devel
BuildRequires: ruby

Requires(pre): systemd-rpm-macros
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd
Requires: jansson
Requires: libstdc++
Requires: libxslt
Requires: libyaml
Requires: openldap
Requires: pcre
Requires: python3
Requires: ruby
Requires: util-linux
Requires: tcp_wrappers
Requires: libxml2
Requires: openssl
Requires: libcap
Requires: systemd

%description
The uWSGI project aims at developing a full stack for building hosting services.
Application servers (for various programming languages and protocols), proxies, process managers
and monitors are all implemented using a common api and a common configuration style.

Thanks to its pluggable architecture it can be extended to support more platforms and languages.
Currently, you can write plugins in C, C++ and Objective-C.

The "WSGI" part in the name is a tribute to the namesake Python standard, as it has been the first developed plugin for the project.
Versatility, performance, low-resource usage and reliability are the strengths of the project (and the only rules followed).

%package        devel
Summary:        Development files for %{name}
Group:          Productivity/Networking/Web/Servers
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains the development header files and libraries
for uWSGI extensions

%package        plugins
Summary:        Plugins for uWSGI
Group:          Productivity/Networking/Web/Servers
Requires:       %{name} = %{version}-%{release}

%description plugins
This package contains all plugins support for uWSGI

%package        python3-plugin
Summary:        Python 3 Plugin for uWSGI
Group:          Productivity/Networking/Web/Servers
Requires:       %{name} = %{version}-%{release}

%description python3-plugin
This package contains support for Python 3 applications via the WSGI protocol.

%prep
%autosetup
cp -p %{SOURCE1} buildconf/

%build
%{python3} uwsgiconfig.py --verbose --build photon.ini
%{python3} uwsgiconfig.py --verbose --plugin plugins/python core

%install
install -d %{buildroot}%{_sysconfdir}/%{name}.d
install -d %{buildroot}%{_includedir}/%{name}
install -d %{buildroot}%{_libdir}/%{name}

install -D -p -m 0755 %{name} %{buildroot}%{_sbindir}/%{name}
install -p -m 0644 *.h %{buildroot}%{_includedir}/%{name}
install -p -m 0755 *_plugin.so %{buildroot}%{_libdir}/%{name}
install -D -p -m 0644 uwsgidecorators.py %{buildroot}%{python3_sitelib}/uwsgidecorators.py
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}.ini
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service

mkdir -p %{buildroot}%{_tmpfilesdir}
cat >> %{buildroot}%{_tmpfilesdir}/%{name}.conf << EOF
d /run/%{name} 0775 %{name} %{name}
EOF
install -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%pre
%sysusers_create_compat %{SOURCE4}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.ini
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%dir %{_sysconfdir}/%{name}.d
%{_sysusersdir}/%{name}.sysusers

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}

%files plugins
%defattr(-,root,root,-)
%{_libdir}/%{name}/airbrake_plugin.so
%{_libdir}/%{name}/alarm_curl_plugin.so
%{_libdir}/%{name}/asyncio_plugin.so
%{_libdir}/%{name}/cache_plugin.so
%{_libdir}/%{name}/carbon_plugin.so
%{_libdir}/%{name}/cgi_plugin.so
%{_libdir}/%{name}/cheaper_backlog2_plugin.so
%{_libdir}/%{name}/cheaper_busyness_plugin.so
%{_libdir}/%{name}/clock_monotonic_plugin.so
%{_libdir}/%{name}/corerouter_plugin.so
%{_libdir}/%{name}/cplusplus_plugin.so
%{_libdir}/%{name}/curl_cron_plugin.so
%{_libdir}/%{name}/dumbloop_plugin.so
%{_libdir}/%{name}/dummy_plugin.so
%{_libdir}/%{name}/emperor_amqp_plugin.so
%{_libdir}/%{name}/fastrouter_plugin.so
%{_libdir}/%{name}/forkptyrouter_plugin.so
%{_libdir}/%{name}/echo_plugin.so
%{_libdir}/%{name}/graylog2_plugin.so
%{_libdir}/%{name}/http_plugin.so
%{_libdir}/%{name}/ldap_plugin.so
%{_libdir}/%{name}/lua_plugin.so
%{_libdir}/%{name}/logcrypto_plugin.so
%{_libdir}/%{name}/logfile_plugin.so
%{_libdir}/%{name}/logpipe_plugin.so
%{_libdir}/%{name}/logsocket_plugin.so
%{_libdir}/%{name}/nagios_plugin.so
%{_libdir}/%{name}/msgpack_plugin.so
%{_libdir}/%{name}/notfound_plugin.so
%{_libdir}/%{name}/pam_plugin.so
%{_libdir}/%{name}/ping_plugin.so
%{_libdir}/%{name}/pty_plugin.so
%{_libdir}/%{name}/rack_plugin.so
%{_libdir}/%{name}/rawrouter_plugin.so
%{_libdir}/%{name}/redislog_plugin.so
%{_libdir}/%{name}/router_access_plugin.so
%{_libdir}/%{name}/router_basicauth_plugin.so
%{_libdir}/%{name}/router_cache_plugin.so
%{_libdir}/%{name}/router_expires_plugin.so
%{_libdir}/%{name}/router_hash_plugin.so
%{_libdir}/%{name}/router_http_plugin.so
%{_libdir}/%{name}/router_memcached_plugin.so
%{_libdir}/%{name}/router_metrics_plugin.so
%{_libdir}/%{name}/router_radius_plugin.so
%{_libdir}/%{name}/router_redirect_plugin.so
%{_libdir}/%{name}/router_redis_plugin.so
%{_libdir}/%{name}/router_rewrite_plugin.so
%{_libdir}/%{name}/router_spnego_plugin.so
%{_libdir}/%{name}/router_static_plugin.so
%{_libdir}/%{name}/router_uwsgi_plugin.so
%{_libdir}/%{name}/router_xmldir_plugin.so
%{_libdir}/%{name}/rpc_plugin.so
%{_libdir}/%{name}/rrdtool_plugin.so
%{_libdir}/%{name}/rsyslog_plugin.so
%{_libdir}/%{name}/signal_plugin.so
%{_libdir}/%{name}/spooler_plugin.so
%{_libdir}/%{name}/sqlite3_plugin.so
%{_libdir}/%{name}/ssi_plugin.so
%{_libdir}/%{name}/sslrouter_plugin.so
%{_libdir}/%{name}/stats_pusher_file_plugin.so
%{_libdir}/%{name}/stats_pusher_socket_plugin.so
%{_libdir}/%{name}/stats_pusher_statsd_plugin.so
%{_libdir}/%{name}/symcall_plugin.so
%{_libdir}/%{name}/syslog_plugin.so
%{_libdir}/%{name}/systemd_logger_plugin.so
%{_libdir}/%{name}/tornado_plugin.so
%{_libdir}/%{name}/transformation_chunked_plugin.so
%{_libdir}/%{name}/transformation_gzip_plugin.so
%{_libdir}/%{name}/transformation_offload_plugin.so
%{_libdir}/%{name}/transformation_template_plugin.so
%{_libdir}/%{name}/transformation_tofile_plugin.so
%{_libdir}/%{name}/transformation_toupper_plugin.so
%{_libdir}/%{name}/tuntap_plugin.so
%{_libdir}/%{name}/ugreen_plugin.so
%{_libdir}/%{name}/webdav_plugin.so
%{_libdir}/%{name}/xattr_plugin.so
%{_libdir}/%{name}/xslt_plugin.so
%{_libdir}/%{name}/zabbix_plugin.so
%{_libdir}/%{name}/zergpool_plugin.so

%files python3-plugin
%defattr(-,root,root,-)
%{_libdir}/%{name}/python_plugin.so
%{python3_sitelib}/uwsgidecorators.py*

%changelog
* Mon Apr 01 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 2.0.21-17
- Bump version as a part of util-linux upgrade
* Thu Mar 28 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 2.0.21-16
- Bump version as a part of libxml2 upgrade
* Mon Mar 04 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 2.0.21-15
- Bump version as a part of sqlite upgrade to v3.43.2
* Tue Feb 20 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 2.0.21-14
- Bump version as a part of libxml2 upgrade
* Sun Nov 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.21-13
- Bump version as a part of openssl upgrade
* Mon Oct 30 2023 Nitesh Kumar <kunitesh@vmware.com> 2.0.21-12
- Bump version as a part of httpd v2.4.58 upgrade
* Tue Sep 19 2023 Nitesh Kumar <kunitesh@vmware.com> 2.0.21-11
- Bump version as a part of openldap v2.6.4 upgrade
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 2.0.21-10
- Resolving systemd-rpm-macros for group creation
* Fri Jul 28 2023 Srish Srinivasan <ssrish@vmware.com> 2.0.21-9
- Bump version as a part of krb5 upgrade
* Wed Apr 19 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.0.21-8
- Bump version as a part of libxml2 upgrade
* Mon Apr 03 2023 Nitesh Kumar <kunitesh@vmware.com> 2.0.21-7
- Bump version as a part of httpd v2.4.56 upgrade
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 2.0.21-6
- Use systemd-rpm-macros for user creation
* Wed Feb 08 2023 Shreenidhi Shedi <sshedi@vmware.com> 2.0.21-5
- Bump version as a part of openldap upgrade
* Tue Jan 31 2023 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 2.0.21-4
- Bump version as a part of krb5 upgrade
* Mon Jan 30 2023 Nitesh Kumar <kunitesh@vmware.com> 2.0.21-3
- Bump version as a part of httpd v2.4.55 upgrade
* Wed Jan 11 2023 Oliver Kurth <okurth@vmware.com> 2.0.21-2
- bump release as part of sqlite update
* Tue Oct 25 2022 Gerrit Photon <photon-checkins@vmware.com> 2.0.21-1
- Automatic Version Bump
* Fri Oct 07 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.0.20-2
- Bump version as a part of libxslt upgrade
* Mon Apr 04 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.20-1
- uwsgi initial build
