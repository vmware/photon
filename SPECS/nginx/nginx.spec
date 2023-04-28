%define njs_ver     0.7.7
%define nginx_user  %{name}

Summary:        High-performance HTTP server and reverse proxy
Name:           nginx
Version:        1.23.1
Release:        4%{?dist}
License:        BSD-2-Clause
URL:            http://nginx.org
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://nginx.org/download/nginx-%{version}.tar.gz
%define sha512 %{name}=62d6b3d5282f4e4cc23adf23b3dc26e06fc4574cae3c18381c406d0cf0f8c68e7dfa86af0c3c1c1485214c548f3b45015eb219e62bfe04e0aaa5edaad82e6706

Source1: https://github.com/nginx/njs/archive/refs/tags/%{name}-njs-%{njs_ver}.tar.gz
%define sha512 %{name}-njs=3fd9e9b84e416e95dbdffced78eabd76a519cccec7c386d8acaccd0d891dea5ceeb702408d4450107c7e3909586753e4eeb5e38c06657cd8f273180beb8fae74

Source2: %{name}.service
Source3: %{name}.sysusers

Patch0: WebCrypto-fixed-dangling-pointer-warning-by-gcc-12.patch

BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  which
BuildRequires:  systemd-devel

Requires: openssl
Requires: pcre
Requires: systemd

Requires(pre): systemd-rpm-macros
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd

%description
NGINX is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server.

%prep
# Using autosetup is not feasible
%setup -q -a0 -a1

pushd njs-%{njs_ver}
%{__patch} -p1 < %{PATCH0}
popd

%build
sh ./configure \
    --prefix=%{_sysconfdir}/%{name} \
    --sbin-path=%{_sbindir}/%{name} \
    --conf-path=/etc/%{name}/%{name}.conf \
    --pid-path=/var/run/%{name}.pid \
    --lock-path=/var/run/%{name}.lock \
    --error-log-path=/var/log/%{name}/error.log \
    --http-log-path=/var/log/%{name}/access.log \
    --add-module=njs-%{njs_ver}/%{name} \
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
%make_install %{?_smp_mflags}
install -vdm755 %{buildroot}%{_unitdir}
install -vdm755 %{buildroot}%{_var}/log
install -vdm755 %{buildroot}%{_var}/opt/%{name}/log
ln -sfv %{_var}/opt/%{name}/log %{buildroot}%{_var}/log/%{name}
install -p -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%clean
rm -rf %{buildroot}

%pre
%sysusers_create_compat %{SOURCE3}

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
%{_sysusersdir}/%{name}.sysusers
%{_sbindir}/*
%{_unitdir}/%{name}.service
%dir %{_var}/opt/%{name}/log
%{_var}/log/%{name}

%changelog
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
