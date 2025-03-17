# References for writing this spec:
# https://github.com/openresty/openresty-packaging/blob/master/rpm/SPECS/openresty.spec
# https://aur.archlinux.org/cgit/aur.git/tree/?h=openresty

%define orprefix    %{_usr}/local/%{name}
%define _cfgdir     %{orprefix}/nginx/conf
%define _tmpdir     %{_sharedstatedir}/%{name}
%define nginx_user  nginx

Summary:        A Fast and Scalable Web Platform by Extending NGINX with Lua
Name:           openresty
Version:        1.21.4.3
Release:        2%{?dist}
URL:            https://openresty.org/en
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://openresty.org/download/%{name}-%{version}.tar.gz

Source1:        %{name}.service
Source2:        %{name}.sh
Source3:        %{name}.sysusers

Source4: license.txt
%include %{SOURCE4}
Patch0:         CVE-2022-41741-and-CVE-2022-41742-nginx.patch

AutoReqProv:    no

Conflicts:      nginx

BuildRequires:  gcc
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  readline-devel
BuildRequires:  zlib-devel
BuildRequires:  systemd-devel
BuildRequires:  perl
BuildRequires:  lua-devel

Requires:       openssl
Requires:       pcre
Requires:       zlib
Requires:       systemd
Requires:       perl
Requires:       lua

Requires(pre):  systemd-rpm-macros
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd

%description
This package contains the core server for OpenResty. Built for production uses.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.

By taking advantage of various well-designed Nginx modules (most of which
are developed by the OpenResty team themselves), OpenResty effectively
turns the nginx server into a powerful web app server, in which the web
developers can use the Lua programming language to script various existing
nginx C modules and Lua modules and construct extremely high-performance
web applications that are capable to handle 10K ~ 1000K+ connections in
a single box.

%package        resty
Summary:        OpenResty command-line utility, resty
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description    resty
This package contains the "resty" command-line utility for OpenResty, which
runs OpenResty Lua scripts on the terminal using a headless NGINX behind the
scene.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.

%package        opm
Summary:        OpenResty Package Manager
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-resty = %{version}-%{release}
Requires:       curl
Requires:       tar
Requires:       gzip
BuildArch:      noarch

%description    opm
This package provides the client side tool, opm, for OpenResty Pakcage Manager (OPM).

%package        doc
Summary:        OpenResty documentation tool, restydoc
Requires:       perl
Requires:       groff
Provides:       restydoc
Provides:       restydoc-index
Provides:       md2pod.pl
BuildArch:      noarch

%description    doc
This package contains the official OpenResty documentation index and
the "restydoc" command-line utility for viewing it.

OpenResty is a full-fledged web platform by integrating the standard Nginx
core, LuaJIT, many carefully written Lua libraries, lots of high quality
3rd-party Nginx modules, and most of their external dependencies. It is
designed to help developers easily build scalable web applications, web
services, and dynamic web gateways.

%prep
%autosetup -p1

%build
perl ./configure \
    --prefix=%{orprefix} \
    --conf-path=%{_cfgdir}/nginx.conf \
    --user=%{nginx_user}\
    --group=%{nginx_user} \
    --with-file-aio \
    --with-http_dav_module \
    --with-http_gzip_static_module \
    --with-http_realip_module \
    --with-http_ssl_module \
    --with-http_stub_status_module \
    --with-mail \
    --with-mail_ssl_module \
    --with-luajit \
    --with-pcre-jit \
    --with-http_v2_module \
    --with-stream \
    --with-threads \
    --with-stream_ssl_module \
    --with-http_iconv_module \
    --with-http_sub_module \
    --with-http_gunzip_module \
    --with-http_auth_request_module \
    -j$(nproc)

%make_build

%install
%make_install %{?_smp_mflags}

rm -rf %{buildroot}%{orprefix}/luajit/share/man \
       %{buildroot}%{orprefix}/luajit/lib/libluajit-5.1.a

mkdir -p %{buildroot}%{_bindir}
ln -sfv %{orprefix}/bin/resty %{buildroot}%{_bindir}
ln -sfv %{orprefix}/bin/opm %{buildroot}%{_bindir}
ln -sfv %{orprefix}/nginx/sbin/nginx %{buildroot}%{_bindir}/%{name}
ln -sfv %{orprefix}/bin/restydoc %{buildroot}%{_bindir}

mkdir -p -m 755 %{buildroot}%{orprefix}/nginx/logs/
install -d %{buildroot}%{_tmpdir}
install -Dm644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
sed -i -e "s|@@ORPREFIX@@|%{orprefix}|" %{buildroot}%{_unitdir}/%{name}.service

install -Dm755 %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh
sed -i -e "s|@@ORPREFIX@@|%{orprefix}|" %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/%{name}.sysusers

%pre
%sysusers_create_compat %{SOURCE3}

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%post
%systemd_post %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{orprefix}/COPYRIGHT
%{_sysconfdir}/profile.d/%{name}.sh
%{_unitdir}/%{name}.service
%{_sysusersdir}/%{name}.sysusers
%exclude %{orprefix}/bin/resty*
%exclude %{orprefix}/bin/opm
%exclude %{orprefix}/bin/md2pod.pl
%exclude %{orprefix}/bin/nginx-xml2pod
%{orprefix}/bin/*
%{_bindir}/%{name}
%{orprefix}/luajit/*
%{orprefix}/lualib/*
%config(noreplace) %{orprefix}/nginx/conf/*
%{orprefix}/nginx/sbin/*
%{orprefix}/nginx/html/*.html
%{orprefix}/nginx/logs
%exclude %dir %{_libdir}/debug

%files resty
%defattr(-,root,root,-)
%{_bindir}/resty
%{orprefix}/bin/resty

%files opm
%defattr(-,root,root,-)
%{_bindir}/opm
%{orprefix}/bin/opm
%{orprefix}/site/manifest/
%{orprefix}/site/pod/

%files doc
%defattr(-,root,root,-)
%{_bindir}/restydoc
%{orprefix}/bin/restydoc
%{orprefix}/bin/restydoc-index
%{orprefix}/bin/md2pod.pl
%{orprefix}/bin/nginx-xml2pod
%{orprefix}/pod/*
%{orprefix}/resty.index

%changelog
* Wed Dec 11 2024 Shreenidhi Shedi <shreenidhi.shedi@broadcom.com> 1.21.4.3-2
- Release bump for SRP compliance
* Wed Jan 03 2024 Michelle Wang <michellew@vmware.com> 1.21.4.3-1
- Upgrade to 1.21.4.3 for CVE-2023-44487
* Tue Aug 08 2023 Mukul Sikka <msikka@vmware.com> 1.21.4.1-9
- Resolving systemd-rpm-macros for group creation
* Mon Jul 17 2023 Michelle Wang <michellew@vmware.com> 1.21.4.1-8
- fix for CVE-2022-41741 and CVE-2022-41742
* Tue Jun 20 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.21.4.1-7
- Bump version as a part of lua upgrade
* Fri Apr 14 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.21.4.1-6
- Bump version as a part of zlib upgrade
* Wed Mar 22 2023 Shreenidhi Shedi <sshedi@vmware.com> 1.21.4.1-5
- Conflict with nginx
* Fri Mar 10 2023 Mukul Sikka <msikka@vmware.com> 1.21.4.1-4
- Use systemd-rpm-macros for user creation
* Tue Dec 20 2022 Guruswamy Basavaiah <bguruswamy@vmware.com> 1.21.4.1-3
- Bump release as a part of readline upgrade
* Thu Dec 08 2022 Dweep Advani <dadvani@vmware.com> 1.21.4.1-2
- Rebuild for perl version upgrade to 5.36.0
* Thu Jul 14 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.21.4.1-1
- Initial version.
