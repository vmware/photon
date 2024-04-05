Summary:        Application Container Server for Networked/Clustered Web Applications
Name:           uwsgi
Version:        2.0.20
Release:        8%{?dist}
License:        GPLv2 with exceptions
Group:          Productivity/Networking/Web/Servers
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://github.com/unbit/uwsgi

Source0: http://projects.unbit.it/downloads/uwsgi-%{version}.tar.gz
%define sha512 uwsgi=22677a8ad1ea886e1a3a153f486474ce064a55e5b12515322345116980f699f4e2e73267f991c300d904284e06f265ea821e71ba3c97832b6f25705475b498ff
Source1: photon.ini
Source2: uwsgi.service
Source3: uwsgi.ini

Patch0: CVE-2023-27522.patch

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
BuildRequires: openldap
BuildRequires: boost-devel
BuildRequires: attr-devel
BuildRequires: libxslt-devel
BuildRequires: systemd-devel
BuildRequires: tcp_wrappers-devel
BuildRequires: ruby

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
%autosetup -p1
cp -p %{SOURCE1} buildconf/

%build
%{__python3} uwsgiconfig.py --verbose --build photon.ini
%{__python3} uwsgiconfig.py --verbose --plugin plugins/python core

%install
install -d %{buildroot}%{_sysconfdir}/uwsgi.d
install -d %{buildroot}%{_includedir}/uwsgi
install -d %{buildroot}%{_libdir}/uwsgi

install -D -p -m 0755 uwsgi %{buildroot}%{_sbindir}/uwsgi
install -p -m 0644 *.h %{buildroot}%{_includedir}/uwsgi
install -p -m 0755 *_plugin.so %{buildroot}%{_libdir}/uwsgi
install -D -p -m 0644 uwsgidecorators.py %{buildroot}%{python3_sitelib}/uwsgidecorators.py
install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/uwsgi.ini
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/uwsgi.service

mkdir -p %{buildroot}%{_tmpfilesdir}
cat >> %{buildroot}%{_tmpfilesdir}/%{name}.conf << EOF
d /run/%{name} 0775 uwsgi uwsgi
EOF

%if 0%{?with_check}
%check
%endif

%pre
getent group uwsgi >/dev/null || groupadd -r uwsgi
getent passwd uwsgi >/dev/null || \
    useradd -c "uWSGI daemon user" -d /run/uwsgi -g %{name} \
        -s /sbin/nologin -M -r %{name}
%post
%systemd_post uwsgi.service

%preun
%systemd_preun uwsgi.service

%postun
%systemd_postun uwsgi.service

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root,-)
%{_sbindir}/uwsgi
%config(noreplace) %{_sysconfdir}/uwsgi.ini
%{_unitdir}/uwsgi.service
%{_tmpfilesdir}/%{name}.conf
%dir %{_sysconfdir}/uwsgi.d
%doc README
%license LICENSE

%files devel
%defattr(-,root,root,-)
%{_includedir}/uwsgi

%files plugins
%defattr(-,root,root,-)
%{_libdir}/uwsgi/airbrake_plugin.so
%{_libdir}/uwsgi/alarm_curl_plugin.so
%{_libdir}/uwsgi/asyncio_plugin.so
%{_libdir}/uwsgi/cache_plugin.so
%{_libdir}/uwsgi/carbon_plugin.so
%{_libdir}/uwsgi/cgi_plugin.so
%{_libdir}/uwsgi/cheaper_backlog2_plugin.so
%{_libdir}/uwsgi/cheaper_busyness_plugin.so
%{_libdir}/uwsgi/clock_monotonic_plugin.so
%{_libdir}/uwsgi/corerouter_plugin.so
%{_libdir}/uwsgi/cplusplus_plugin.so
%{_libdir}/uwsgi/curl_cron_plugin.so
%{_libdir}/uwsgi/dumbloop_plugin.so
%{_libdir}/uwsgi/dummy_plugin.so
%{_libdir}/uwsgi/emperor_amqp_plugin.so
%{_libdir}/uwsgi/fastrouter_plugin.so
%{_libdir}/uwsgi/forkptyrouter_plugin.so
%{_libdir}/uwsgi/echo_plugin.so
%{_libdir}/uwsgi/graylog2_plugin.so
%{_libdir}/uwsgi/http_plugin.so
%{_libdir}/uwsgi/ldap_plugin.so
%{_libdir}/uwsgi/lua_plugin.so
%{_libdir}/uwsgi/logcrypto_plugin.so
%{_libdir}/uwsgi/logfile_plugin.so
%{_libdir}/uwsgi/logpipe_plugin.so
%{_libdir}/uwsgi/logsocket_plugin.so
%{_libdir}/uwsgi/nagios_plugin.so
%{_libdir}/uwsgi/msgpack_plugin.so
%{_libdir}/uwsgi/notfound_plugin.so
%{_libdir}/uwsgi/pam_plugin.so
%{_libdir}/uwsgi/ping_plugin.so
%{_libdir}/uwsgi/pty_plugin.so
%{_libdir}/uwsgi/rack_plugin.so
%{_libdir}/uwsgi/rawrouter_plugin.so
%{_libdir}/uwsgi/redislog_plugin.so
%{_libdir}/uwsgi/router_access_plugin.so
%{_libdir}/uwsgi/router_basicauth_plugin.so
%{_libdir}/uwsgi/router_cache_plugin.so
%{_libdir}/uwsgi/router_expires_plugin.so
%{_libdir}/uwsgi/router_hash_plugin.so
%{_libdir}/uwsgi/router_http_plugin.so
%{_libdir}/uwsgi/router_memcached_plugin.so
%{_libdir}/uwsgi/router_metrics_plugin.so
%{_libdir}/uwsgi/router_radius_plugin.so
%{_libdir}/uwsgi/router_redirect_plugin.so
%{_libdir}/uwsgi/router_redis_plugin.so
%{_libdir}/uwsgi/router_rewrite_plugin.so
%{_libdir}/uwsgi/router_spnego_plugin.so
%{_libdir}/uwsgi/router_static_plugin.so
%{_libdir}/uwsgi/router_uwsgi_plugin.so
%{_libdir}/uwsgi/router_xmldir_plugin.so
%{_libdir}/uwsgi/rpc_plugin.so
%{_libdir}/uwsgi/rrdtool_plugin.so
%{_libdir}/uwsgi/rsyslog_plugin.so
%{_libdir}/uwsgi/signal_plugin.so
%{_libdir}/uwsgi/spooler_plugin.so
%{_libdir}/uwsgi/sqlite3_plugin.so
%{_libdir}/uwsgi/ssi_plugin.so
%{_libdir}/uwsgi/sslrouter_plugin.so
%{_libdir}/uwsgi/stats_pusher_file_plugin.so
%{_libdir}/uwsgi/stats_pusher_socket_plugin.so
%{_libdir}/uwsgi/stats_pusher_statsd_plugin.so
%{_libdir}/uwsgi/symcall_plugin.so
%{_libdir}/uwsgi/syslog_plugin.so
%{_libdir}/uwsgi/systemd_logger_plugin.so
%{_libdir}/uwsgi/tornado_plugin.so
%{_libdir}/uwsgi/transformation_chunked_plugin.so
%{_libdir}/uwsgi/transformation_gzip_plugin.so
%{_libdir}/uwsgi/transformation_offload_plugin.so
%{_libdir}/uwsgi/transformation_template_plugin.so
%{_libdir}/uwsgi/transformation_tofile_plugin.so
%{_libdir}/uwsgi/transformation_toupper_plugin.so
%{_libdir}/uwsgi/tuntap_plugin.so
%{_libdir}/uwsgi/ugreen_plugin.so
%{_libdir}/uwsgi/webdav_plugin.so
%{_libdir}/uwsgi/xattr_plugin.so
%{_libdir}/uwsgi/xslt_plugin.so
%{_libdir}/uwsgi/zabbix_plugin.so
%{_libdir}/uwsgi/zergpool_plugin.so

%files python3-plugin
%defattr(-,root,root,-)
%{_libdir}/uwsgi/python_plugin.so
%{python3_sitelib}/uwsgidecorators.py*

%changelog
* Fri Apr 05 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 2.0.20-8
- Version Bump up to consume httpd v2.4.59
* Mon Oct 30 2023 Nitesh Kumar <kunitesh@vmware.com> 2.0.20-7
- Bump version as a part of httpd v2.4.58 upgrade
* Tue Aug 29 2023 Piyush Gupta <gpiyush@vmware.com> 2.0.20-6
- Fix CVE-2023-27522.
* Mon May 29 2023 Harinadh D <hdommaraju@vmware.com> 2.0.20-5
- Version bump to use curl 8.1.1
* Tue Apr 04 2023 Harinadh D <hdommaraju@vmware.com> 2.0.20-4
- version bump to use curl 8.0.1
* Mon Apr 03 2023 Nitesh Kumar <kunitesh@vmware.com> 2.0.20-3
- Bump version as a part of httpd v2.4.56 upgrade
* Mon Jan 30 2023 Nitesh Kumar <kunitesh@vmware.com> 2.0.20-2
- Bump version as a part of httpd v2.4.55 upgrade
* Mon Apr 04 2022 Prashant S Chauhan <psinghchauha@vmware.com> 2.0.20-1
- uwsgi initial build
