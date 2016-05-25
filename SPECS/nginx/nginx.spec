Summary:	High-performance HTTP server and reverse proxy
Name:		nginx
Version:	1.10.0
Release:	2%{?dist}
License:	BSD-2-Clause
URL:		http://nginx.org/download/nginx-1.10.0.tar.gz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: Photon
Source0:	%{name}-%{version}.tar.gz
%define sha1 nginx=7a452cfe37e4134481442dbfa3fbdac6f484c5bc

BuildRequires:	openssl-devel
BuildRequires:  pcre-devel
%description
NGINX is a free, open-source, high-performance HTTP server and reverse proxy, as well as an IMAP/POP3 proxy server. 

%prep
%setup -q
%build
./configure \
	--prefix=%{_sysconfdir}//nginx              \
	--sbin-path=/usr/sbin/nginx                 \
	--conf-path=/etc/nginx/nginx.conf           \
	--pid-path=/var/run/nginx/nginx.pid         \
	--lock-path=/var/run/nginx/nginx.lock       \
	--error-log-path=/var/log/nginx/error.log   \
	--http-log-path=/var/log/nginx/access.log   \
    --with-http_ssl_module \
    --with-pcre \
    --with-ipv6 

make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
install -vdm755 %{buildroot}/usr/lib/systemd/system
install -vdm755 %{buildroot}%{_var}/log/nginx
install -vdm755 %{buildroot}%{_var}/run/nginx

cat << EOF >> %{buildroot}/usr/lib/systemd/system/nginx.service
[Unit]
Description=Nginx High-performance HTTP server and reverse proxy
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/var/run/nginx/nginx.pid
ExecStartPre=/usr/sbin/nginx -t
ExecStart=/usr/sbin/nginx
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s QUIT $MAINPID
PrivateTmp=true
[Install]
WantedBy=multi-user.target

EOF

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root)
%{_sysconfdir}/*
%{_sbindir}/*
%{_libdir}/*
%{_var}/log/nginx
%{_var}/run/nginx

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	1.10.0-2
-	GA - Bump release of all rpms
*   Mon May 16 2016 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-1
-	Initial build. First version
