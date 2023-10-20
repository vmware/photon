%define njs_ver 0.7.5
%define nginx_user %{name}

Summary:        High-performance HTTP server and reverse proxy
Name:           nginx
Version:        1.22.0
Release:        3%{?dist}
License:        BSD-2-Clause
URL:            http://nginx.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        http://nginx.org/download/%{name}-%{version}.tar.gz
%define sha512 %{name}=074782dba9cd5f8f493fbb57e20bda6dc9171814d919a47ee9f825d93f12c9f9d496e25d063c983191b55ad6a236bcef252ce16ecc1d253dc8b23433557559b1

Source1:        https://github.com/nginx/njs/archive/refs/tags/%{name}-njs-%{njs_ver}.tar.gz
%define sha512  %{name}-njs=e33dbb285ff6216acddcd213fdbd73ffadd5730680bcec742b1598fa57b4d100da32c913b1c2648b3e87867fc29bf11075d70fa5655f85c62e42eb0a48d177f1

Source2:        %{name}.service

Patch0: CVE-2022-41741-41742.patch
Patch1: CVE-2023-44487.patch

BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  which
BuildRequires:  systemd-devel

Requires: openssl
Requires: pcre
Requires: systemd

Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd

%description
NGINX is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server.

%prep
%autosetup -a0 -a1 -p1

%build
sh ./configure \
    --prefix=%{_sysconfdir}/nginx \
    --sbin-path=%{_sbindir}/nginx \
    --conf-path=/etc/nginx/nginx.conf \
    --pid-path=/var/run/nginx.pid \
    --lock-path=/var/run/nginx.lock \
    --error-log-path=/var/log/nginx/error.log \
    --http-log-path=/var/log/nginx/access.log \
    --add-module=njs-%{njs_ver}/nginx \
    --with-http_ssl_module \
    --with-pcre \
    --with-ipv6 \
    --with-stream \
    --with-http_auth_request_module \
    --with-http_sub_module \
    --with-http_stub_status_module \
    --with-http_v2_module \
    --with-http_realip_module \
    --user=%{nginx_user} \
    --group=%{nginx_user}

%make_build

%install
%make_install
install -vdm755 %{buildroot}%{_unitdir}
install -vdm755 %{buildroot}%{_var}/log
install -vdm755 %{buildroot}%{_var}/opt/nginx/log
install -p -d -m 0700 %{buildroot}%{_sharedstatedir}/%{name}
ln -sfrv %{buildroot}%{_var}/opt/nginx/log %{buildroot}%{_var}/log/nginx
install -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service

%clean
rm -rf %{buildroot}

%pre
getent group %{nginx_user} > /dev/null || groupadd -r %{nginx_user}

getent passwd %{nginx_user} > /dev/null || \
  useradd -r -d %{_sharedstatedir}/nginx -g %{nginx_user} \
    -s /sbin/nologin -c "Nginx web server" %{nginx_user}

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%post
%systemd_post %{name}.service

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
%config(noreplace) %{_sysconfdir}/%{name}/nginx.conf
%config(noreplace) %{_sysconfdir}/%{name}/nginx.conf.default
%config(noreplace) %{_sysconfdir}/%{name}/scgi_params
%config(noreplace) %{_sysconfdir}/%{name}/scgi_params.default
%config(noreplace) %{_sysconfdir}/%{name}/uwsgi_params
%config(noreplace) %{_sysconfdir}/%{name}/uwsgi_params.default
%{_sysconfdir}/%{name}/win-utf
%{_sysconfdir}/%{name}/html/*
%{_sbindir}/*
%{_unitdir}/%{name}.service
%dir %{_var}/opt/nginx/log
%{_var}/log/nginx

%changelog
* Fri Oct 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.22.0-3
- Fix CVE-2023-44487
* Tue Feb 21 2023 Brian Munro <bmunro-peralex@github.com> 1.22.0-2
- Enable http_realip_module
* Wed Oct 26 2022 Keerthana K <keerthanak@vmware.com> 1.22.0-1
- Update to 1.22.0 and Fix CVE-2022-41741 CVE-2022-41742
* Mon Jul 18 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.16.1-7
- Fix sevice handling and run in nginx user context
* Tue Apr 12 2022 Nitesh Kumar <kunitesh@vmware.com> 1.16.1-6
- Fix for CVE-2021-3618
* Thu Dec 16 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.16.1-5
- Fix nginx service handling
* Wed May 19 2021 Keerthana K <keerthanak@vmware.com> 1.16.1-4
- Fix for CVE-2021-23017
* Mon May 04 2020 Keerthana K <keerthanak@vmware.com> 1.16.1-3
- Adding http v2 module support.
* Tue Feb 11 2020 Ankit Jain <ankitja@vmware.com> 1.16.1-2
- Fix for CVE-2019-20372
* Thu Aug 29 2019 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.16.1-1
- Update to version 1.16.1-1
* Fri Mar 15 2019 Keerthana K <keerthanak@vmware.com> 1.15.3-6
- Enable https_stub_status_module.
* Mon Feb 25 2019 Ankit Jain <ankitja@vmware.com> 1.15.3-5
- Fix for CVE-2018-16843 and CVE-2018-16844
* Thu Feb 21 2019 Siju Maliakkal <smaliakkal@vmware.com> 1.15.3-4
- Fix CVE-2018-16845
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
