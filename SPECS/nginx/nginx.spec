Summary:        High-performance HTTP server and reverse proxy
Name:           nginx
Version:        1.15.3
Release:        2%{?dist}
License:        BSD-2-Clause
URL:            http://nginx.org/download/nginx-%{version}.tar.gz
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1    nginx=584a585096cffa240a6224f718b4c0c83a7a5e36
Source1:        nginx.service
Source2:        nginx-njs-0.2.1.tar.gz
%define sha1    nginx-njs=fd8c3f2d219f175be958796e3beaa17f3b465126
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  which
%description
NGINX is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server.

%prep
%setup -q
pushd ../
mkdir nginx-njs
tar -C nginx-njs -xf %{SOURCE2}
popd

%build
./configure \
    --prefix=%{_sysconfdir}//nginx              \
    --sbin-path=/usr/sbin/nginx                 \
    --conf-path=/etc/nginx/nginx.conf           \
    --pid-path=/var/run/nginx.pid               \
    --lock-path=/var/run/nginx.lock             \
    --error-log-path=/var/log/nginx/error.log   \
    --http-log-path=/var/log/nginx/access.log   \
    --add-module=../nginx-njs/njs-0.2.1/nginx   \
    --with-http_ssl_module \
    --with-pcre \
    --with-ipv6 \
    --with-stream \
    --with-http_auth_request_module \
    --with-http_sub_module

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm755 %{buildroot}/usr/lib/systemd/system
install -vdm755 %{buildroot}%{_var}/log
install -vdm755 %{buildroot}%{_var}/opt/nginx/log
ln -sfv %{_var}/opt/nginx/log %{buildroot}%{_var}/log/nginx
install -p -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/nginx.service

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_sbindir}/*
%{_libdir}/systemd/system/nginx.service
%dir %{_var}/opt/nginx/log
%{_var}/log/nginx

%changelog
*   Mon Sep 17 2018 Keerthana K <keerthanak@vmware.com> 1.15.3-2
-   Adding http_auth_request_module and http_sub_module.
*   Fri Sep 7 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.15.3-1
-   Upgrade to version 1.15.3
*   Fri Jul 20 2018 Keerthana K <keerthanak@vmware.com> 1.13.8-3
-   Restarting nginx on failure.
*   Fri Jun 08 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.13.8-2
-   adding module njs.
*   Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.13.8-1
-   Update to version 1.13.8 to support nginx-ingress
*   Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  1.13.5-2
-   Fixed the log file directory structure
*   Wed Oct 04 2017 Xiaolin Li <xiaolinl@vmware.com> 1.13.5-1
-   Update to version 1.13.5
*   Mon May 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.11.13-2
-   adding module stream to nginx.
*   Wed Apr 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11.13-1
-   update to 1.11.13
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.10.0-5
-   Add patch for CVE-2016-4450
*   Wed Jul 27 2016 Divya Thaluru<dthaluru@vmware.com> 1.10.0-4
-   Removed packaging of debug files
*   Fri Jul 8 2016 Divya Thaluru<dthaluru@vmware.com> 1.10.0-3
-   Modified default pid filepath and fixed nginx systemd service
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.10.0-2
-   GA - Bump release of all rpms
*   Mon May 16 2016 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-1
-   Initial build. First version
