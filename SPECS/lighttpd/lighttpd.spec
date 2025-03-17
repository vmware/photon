%define documentroot /srv/www/htdocs
Summary:        A secure, fast, compliant, and very flexible web server
Name:           lighttpd
Version:        1.4.76
Release:        2%{?dist}
URL:            https://www.lighttpd.net/
Group:          Productivity/Networking/Web/Servers
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://download.lighttpd.net/lighttpd/releases-1.4.x/%{name}-%{version}.tar.gz
Source1: %{name}.sysusers
Source2: %{name}.logrotate
Source3: %{name}.service
Source4: start-server.sh

Source5: license.txt
%include %{SOURCE5}

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  m4
BuildRequires:  lua-devel
BuildRequires:  glibc-devel
BuildRequires:  c-ares-devel
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  pcre2-devel
BuildRequires:  systemd-devel

Requires:       openssl
Requires:       c-ares
Requires:       curl
Requires:       lua
Requires:       systemd
Requires:       logrotate
Requires(pre):  systemd-rpm-macros
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd

%description
lighttpd a secure, fast, compliant and very flexible web-server
which has been optimized for high-performance environments. It has a very
low memory footprint compared to other webservers and takes care of cpu-load.
Its advanced feature-set (FastCGI, CGI, Auth, Output-Compression,
URL-Rewriting and many more) make lighttpd the perfect webserver-software
for every server that is suffering load problems.

%prep
%autosetup -p1

%build
export LIBS='-lssl -lcrypto -lcurl -lcares -lz -lglib-2.0 -lgthread-2.0 -lpcre -lstdc++'
./autogen.sh
%configure \
    --bindir=%{_sbindir}        \
    --libdir=%{_libdir}/%{name} \
    --enable-ipv6               \
    --with-openssl              \
    --with-lua                  \
    --with-pcre

%make_build

%install
%make_install %{?_smp_mflags}

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.sysusers
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0755 %{SOURCE4} %{buildroot}%{_libexecdir}/%{name}/start-server.sh
install -vdm755 %{buildroot}%{_presetdir}
echo "disable %{name}.service" > %{buildroot}%{_presetdir}/50-%{name}.preset

mkdir -p %{buildroot}%{_sysconfdir}/%{name}/ \
         %{buildroot}%{_var}/log/%{name} \
         %{buildroot}%{_sharedstatedir}/%{name}/ \
         %{buildroot}%{documentroot}

cp -r doc/config/* %{buildroot}%{_sysconfdir}/%{name}/

find %{buildroot}%{_sysconfdir}/%{name}/ \( -name "Makefile*" -o -name "*.template" \) -delete

%check
make %{?_smp_mflags} check

%pre
%sysusers_create_compat %{SOURCE1}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license COPYING
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/conf.d/
%dir %{_sysconfdir}/%{name}/vhosts.d/
%attr(0750, %{name}, %{name}) %{_sharedstatedir}/%{name}/
%attr(0750, %{name}, %{name}) %{_var}/log/%{name}/
%attr(0750, %{name}, %{name}) %dir %{documentroot}
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %{_sysconfdir}/%{name}/conf.d/*.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sbindir}/%{name}
%{_sbindir}/%{name}-angel
%{_libdir}/%{name}/
%{_libexecdir}/%{name}/
%{_presetdir}/50-%{name}.preset
%{_sysusersdir}/%{name}.sysusers
%{_unitdir}/%{name}.service
%{_mandir}/man8/%{name}*8*

%changelog
* Wed Dec 11 2024 Ajay Kaher <ajay.kaher@broadcom.com> 1.4.76-2
- Release bump for SRP compliance
* Mon May 20 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 1.4.76-1
- Initial Build.
