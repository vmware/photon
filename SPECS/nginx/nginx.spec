Summary:        High-performance HTTP server and reverse proxy
Name:           nginx
Version:        1.13.8
Release:        4%{?dist}
License:        BSD-2-Clause
URL:            http://nginx.org/download/nginx-%{version}.tar.gz
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        %{name}-%{version}.tar.gz
%define sha1    nginx=a1f9348c9c46f449a0b549d0519dd34191d30cee
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
install -vdm755 %{buildroot}%{_var}/log/nginx
install -p -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/nginx.service

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_sbindir}/*
%{_libdir}/systemd/system/nginx.service
%dir %{_var}/log/nginx

%changelog
*   Mon Sep 10 2018 Keerthana K <keerthanak@vmware.com> 1.13.8-4
-   Adding http_auth_request_module and http_sub_module.
*   Fri Jul 20 2018 Keerthana K <keerthanak@vmware.com> 1.13.8-3
-   Restarting nginx service on failure.
*   Fri Jun 08 2018 Dheeraj Shetty <dheerajs@vmware.com> 1.13.8-2
-   adding module njs.
*   Fri May 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.13.8-1
-   Update to version 1.13.8 to support nginx-ingress
*   Tue Oct 17 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.11.13-4
-   Add patch for CVE-2017-7529
*   Fri Jun 23 2017 Divya Thaluru <dthaluru@vmware.com> 1.11.13-3
-   Removed packaging of debug files
*   Mon May 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.11.13-2
-   adding module stream to nginx.
*   Wed Apr 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.11.13-1
-   update to 1.11.13
*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  1.10.0-4
-   Add patch for CVE-2016-4450
*   Fri Jul 8 2016 Divya Thaluru<dthaluru@vmware.com> 1.10.0-3
-   Modified default pid filepath and fixed nginx systemd service
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.10.0-2
-   GA - Bump release of all rpms
*   Mon May 16 2016 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-1
-   Initial build. First version
