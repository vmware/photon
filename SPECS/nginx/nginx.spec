%define njs_ver     0.8.4
%define nginx_user  %{name}
%define headers_more_nginx_module_ver 0.37
%define dyn_modules_dir     %{_sysconfdir}/%{name}/modules

Summary:        High-performance HTTP server and reverse proxy
Name:           nginx
Epoch:          1
Version:        1.26.2
Release:        5%{?dist}
URL:            http://nginx.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://nginx.org/download/nginx-%{version}.tar.gz

Source1: https://github.com/nginx/njs/archive/refs/tags/%{name}-njs-%{njs_ver}.tar.gz

Source2: https://github.com/openresty/headers-more-nginx-module/archive/refs/tags/headers-more-nginx-module-%{headers_more_nginx_module_ver}.tar.gz

Source3: %{name}.service
Source4: %{name}.sysusers

Source5: license.txt
%include %{SOURCE5}

Patch0: convert-to-dynamic.patch

BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  which
BuildRequires:  systemd-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel

Requires: openssl
Requires: pcre
Requires: systemd

Requires(pre): systemd-rpm-macros
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd

%description
NGINX is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server.

%package mod-njs
Summary: nginx javascript module

%description mod-njs
njs is an nginx module that extends the server's functionality through JavaScript scripting,
enabling the creation of custom server-side logic and more.

%package mod-headers-more
Summary: Set, add, and clear arbitrary output headers in NGINX http servers
Requires: %{name} = %{epoch}:%{version}-%{release}
Conflicts: %{name} < 1:1.26.2-4%{?dist}

%description mod-headers-more
%{summary}.

%package mod-stream
Summary: Nginx stream modules
Requires: %{name} = %{epoch}:%{version}-%{release}

%description mod-stream
%{summary}.

%package mod-http-dav
Summary: File management automation via the WebDAV protocol.
Requires: %{name} = %{epoch}:%{version}-%{release}

%description mod-http-dav
%{summary}.

%package mod-stream-ssl-preread
Summary: Allows extracting information from the ClientHello message without terminating SSL/TLS
Requires: %{name} = %{epoch}:%{version}-%{release}

%description mod-stream-ssl-preread
%{summary}.

%package all-modules
Summary: A meta package that installs all available Nginx modules
Requires: %{name} = %{epoch}:%{version}-%{release}

BuildArch: noarch

Requires: %{name}-mod-njs = %{epoch}:%{version}-%{release}
Requires: %{name}-mod-stream = %{epoch}:%{version}-%{release}
Requires: %{name}-mod-http-dav = %{epoch}:%{version}-%{release}
Requires: %{name}-mod-headers-more = %{epoch}:%{version}-%{release}
Requires: %{name}-mod-stream-ssl-preread = %{epoch}:%{version}-%{release}

%description all-modules
%{summary}.

%prep
# Using autosetup is not feasible
%setup -q -a1 -a2
%autopatch -p1

%build
export CFLAGS="-O2 -g -Wno-discarded-qualifiers"
sh ./configure \
    --prefix=%{_sysconfdir}/%{name} \
    --sbin-path=%{_sbindir}/%{name} \
    --conf-path=%{_sysconfdir}/%{name}/%{name}.conf \
    --pid-path=%{_var}/run/%{name}.pid \
    --lock-path=%{_var}/run/%{name}.lock \
    --error-log-path=%{_var}/log/%{name}/error.log \
    --http-log-path=%{_var}/log/%{name}/access.log \
    --user=%{nginx_user} \
    --group=%{nginx_user} \
    --add-dynamic-module=njs-%{njs_ver}/%{name} \
    --add-dynamic-module=./headers-more-nginx-module-%{headers_more_nginx_module_ver} \
    --with-pcre \
    --with-compat \
    --with-http_ssl_module \
    --modules-path=%{dyn_modules_dir} \
    --with-http_auth_request_module \
    --with-http_sub_module \
    --with-http_stub_status_module \
    --with-http_v2_module \
    --with-http_realip_module \
    --with-http_dav_module=dynamic \
    --with-stream=dynamic \
    --with-stream_ssl_preread_module=dynamic

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm755 %{buildroot}%{_unitdir}
install -vdm755 %{buildroot}%{_var}/log
install -vdm755 %{buildroot}%{_var}/opt/%{name}/log
ln -sfrv %{buildroot}%{_var}/opt/%{name}/log %{buildroot}%{_var}/log/%{name}
install -p -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysusersdir}/%{name}.conf

%clean
rm -rf %{buildroot}

%pre
%sysusers_create_compat %{SOURCE4}

%post
%systemd_post %{name}.service

%postun
%systemd_postun %{name}.service

%preun
%systemd_preun %{name}.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi.conf
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi.conf.default
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi_params
%config(noreplace) %{_sysconfdir}/%{name}/fastcgi_params.default
%config(noreplace) %{_sysconfdir}/%{name}/koi-utf
%config(noreplace) %{_sysconfdir}/%{name}/koi-win
%config(noreplace) %{_sysconfdir}/%{name}/mime.types
%config(noreplace) %{_sysconfdir}/%{name}/mime.types.default
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf.default
%config(noreplace) %{_sysconfdir}/%{name}/scgi_params
%config(noreplace) %{_sysconfdir}/%{name}/scgi_params.default
%config(noreplace) %{_sysconfdir}/%{name}/uwsgi_params
%config(noreplace) %{_sysconfdir}/%{name}/uwsgi_params.default
%{_sysconfdir}/%{name}/win-utf
%{_sysconfdir}/%{name}/html/*
%{_sysusersdir}/%{name}.conf
%{_sbindir}/*
%{_unitdir}/%{name}.service
%dir %{_var}/opt/%{name}/log
%{_var}/log/%{name}

%files all-modules
%defattr(-,root,root)

%files mod-njs
%defattr(-,root,root)
%{dyn_modules_dir}/ngx_http_js_module.so
%{dyn_modules_dir}/ngx_stream_js_module.so

%files mod-headers-more
%defattr(-,root,root)
%{dyn_modules_dir}/ngx_http_headers_more_filter_module.so

%files mod-stream
%defattr(-,root,root)
%{dyn_modules_dir}/ngx_stream_module.so

%files mod-http-dav
%defattr(-,root,root)
%{dyn_modules_dir}/ngx_http_dav_module.so

%files mod-stream-ssl-preread
%defattr(-,root,root)
%{dyn_modules_dir}/ngx_stream_ssl_preread_module.so

%changelog
* Thu May 08 2025 Mukul Sikka <mukul.sikka@broadcom.com> 1.26.2-5
- Renaming sysusers to conf to fix auto user creation
* Mon Jan 06 2025 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.26.2-4
- Convert modulee like http-dav and stream-ssl-preread to dynamic
- Package dynamic modules as a sub package
* Thu Dec 12 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.26.2-3
- Release bump for SRP compliance
* Fri Oct 4 2024 Etienne Le Sueur <etienne.le-sueur@broadcom.com> 1.26.2-2
- Include WebDAV module
* Tue Aug 13 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.26.2-1
- Downgrade version to v1.26.2
- Adding Epoch to consider v1.26.2 latest instead of v1.27.0
- nginx don't maintain stable branch for odd releases
- Fix CVE-2024-7347
* Wed Jun 19 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.27.0-1
- Version upgrade to v1.27.0 to fix following issues:
- Add headers-more-nginx-module
- CVE-2024-31079, CVE-2024-32760, CVE-2024-34161 and CVE-2024-35200
* Wed May 15 2024 Mukul Sikka <mukul.sikka@broadcom.com> 1.25.2-4
- Enable support for ssl_preread_module
* Tue Mar 12 2024 Ashwin Dayanand Kamat <ashwin.kamat@broadcom.com> 1.25.2-3
- Bump version as a part of libxml2 upgrade
* Thu Oct 19 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.25.2-2
- Fix CVE-2023-44487
* Tue Aug 22 2023 Harinadh D <hdommaraju@vmware.com> 1.25.2-1
- Version upgrade
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 1.23.1-5
- Resolving systemd-rpm-macros for group creation
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 1.23.1-4
- Use systemd-rpm-macros for user creation
* Mon Feb 20 2023 Harinadh D <hdommaraju@vmware.com> 1.23.1-3
- enable http_realip_module
- Author: Brian Munro <bmunro-peralex>
* Thu Oct 20 2022 Vamsi Krishna Brahmajosyula <vbrahmajosyula@vmware.com> 1.23.1-2
- Fix build with latest toolchain
* Tue Oct 04 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.23.1-1
- Upgrade nginx to v1.23.1
- Upgrade nginx-njs to v0.7.7
* Mon Aug 22 2022 Harinadh D <hdommaraju@vmware.com> 1.22.0-1
- version update
- security support is ended for version 1.21
* Tue Aug 16 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.21.0-2
- Fix sevice handling and run in nginx user context
* Tue Apr 12 2022 Nitesh Kumar <kunitesh@vmware.com> 1.21.0-1
- Upgrade to v1.21.0, Address CVE-2021-3618
* Thu Dec 16 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.20.2-1
- Fix nginx service handling
- Upgrade to v1.20.2
* Mon Nov 29 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.20.0-3
- Increment for openssl 3.0.0 compatibility
* Mon May 24 2021 Keerthana K <keerthanak@vmware.com> 1.20.0-2
- Fix for CVE-2021-23017
* Tue Apr 20 2021 Gerrit Photon <photon-checkins@vmware.com> 1.20.0-1
- Automatic Version Bump
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.19.10-1
- Automatic Version Bump
* Tue Sep 29 2020 Gerrit Photon <photon-checkins@vmware.com> 1.19.3-1
- Automatic Version Bump
* Tue Sep 29 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.19.2-2
- openssl 1.1.1
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.19.2-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.19.0-1
- Automatic Version Bump
* Mon May 04 2020 Keerthana K <keerthanak@vmware.com> 1.16.1-2
- Adding http v2 module support.
* Mon Oct 14 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.16.1-1
- update version to 1.16.1
* Fri Mar 15 2019 Keerthana K <keerthanak@vmware.com> 1.15.3-4
- Enable http_stub_status_module.
* Wed Nov 07 2018 Ajay Kaher <akaher@vmware.com> 1.15.3-3
- mark config files as non replaceable on upgrade.
* Mon Sep 17 2018 Keerthana K <keerthanak@vmware.com> 1.15.3-2
- Adding http_auth_request_module and http_sub_module.
* Fri Sep 7 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.15.3-1
- Upgrade to version 1.15.3
* Fri Jul 20 2018 Keerthana K <keerthanak@vmware.com> 1.13.8-3
- Restarting nginx on failure.
* Fri Jun 08 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.13.8-2
- adding module njs.
* Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.13.8-1
- Update to version 1.13.8 to support nginx-ingress
* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  1.13.5-2
- Fixed the log file directory structure
* Wed Oct 04 2017 Xiaolin Li <xiaolinl@vmware.com> 1.13.5-1
- Update to version 1.13.5
* Mon May 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.11.13-2
- adding module stream to nginx.
* Wed Apr 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11.13-1
- update to 1.11.13
* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.10.0-5
- Add patch for CVE-2016-4450
* Wed Jul 27 2016 Divya Thaluru<dthaluru@vmware.com> 1.10.0-4
- Removed packaging of debug files
* Fri Jul 8 2016 Divya Thaluru<dthaluru@vmware.com> 1.10.0-3
- Modified default pid filepath and fixed nginx systemd service
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.10.0-2
- GA - Bump release of all rpms
* Mon May 16 2016 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-1
- Initial build. First version
