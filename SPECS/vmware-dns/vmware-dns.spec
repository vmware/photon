Name:          vmware-dns
Summary:       DNS Service
Version:       1.2.0
Release:       1%{?dist}
License:       Apache 2.0
Group:         Applications/System
Vendor:        VMware, Inc.
URL: 	       https://github.com/vmware/lightwave
Source0:       lightwave-%{version}.tar.gz
%define sha1 lightwave=223d98f15b67f531fc8eeed824756cb313a2ac01
Distribution:  Photon
Requires:  coreutils >= 8.22
Requires:  openssl >= 1.0.2, krb5 >= 1.14
Requires:  cyrus-sasl >= 2.1
Requires:  likewise-open >= 6.2.11
BuildRequires:  coreutils >= 8.22, openssl-devel >= 1.0.2
BuildRequires:  krb5-devel >= 1.14, cyrus-sasl >= 2.1
BuildRequires:  likewise-open-devel >= 6.2.10
BuildRequires:  vmware-directory-client-devel = %{version}

%if 0%{?_sasl_prefix:1} == 0
%define _sasl_prefix /usr
%endif

%if 0%{?_krb5_prefix:1} == 0
%define _krb5_prefix /usr
%endif

%if 0%{?_likewise_open_prefix:1} == 0
%define _likewise_open_prefix /opt/likewise
%endif

%define _likewise_open_bindir %{_likewise_open_prefix}/bin
%define _likewise_open_sbindir %{_likewise_open_prefix}/sbin

%define _krb5_lib_dir %{_krb5_prefix}/lib64
%define _krb5_gss_conf_dir /etc/gss
%define _logdir /var/log/lightwave
%define _logconfdir /etc/syslog-ng/lightwave.conf.d

%define _prefix /opt/vmware
%define _includedir %{_prefix}/include
%define _lib64dir %{_prefix}/lib64
%define _bindir %{_prefix}/bin
%define _sbindir %{_prefix}/sbin
%define _datadir %{_prefix}/share

%description
VMware DNS Service

%package client
Summary: VMware DNS Client
Requires:  coreutils >= 8.22, openssl >= 1.0.2, krb5 >= 1.14, cyrus-sasl >= 2.1, likewise-open >= 6.2.9
%description client
Client libraries to communicate with DNS Service

%package client-devel
Summary: VMware DNS Client Development Library
Requires: vmware-dns-client = %{version}
%description client-devel
Development Libraries to communicate with DNS Service

%prep
%setup -qn lightwave-%{version}

%build
export CFLAGS="-Wno-unused-but-set-variable -Wno-pointer-sign -Wno-implicit-function-declaration -Wno-address -Wno-enum-compare"
cd vmdns/build
autoreconf -mif ..
../configure \
    --prefix=%{_prefix} \
    --libdir=%{_lib64dir} \
    --localstatedir=%{_localstatedir}/lib/vmware/vmdir \
    --with-vmdir=%{_prefix} \
    --with-likewise=%{_likewise_open_prefix} \
    --with-ssl=/usr 
make

%install

[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
cd vmdns/build && make install DESTDIR=$RPM_BUILD_ROOT

%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
        # Not in chroot
        if [ -z "`pidof lwsmd`" ]; then
            /bin/systemctl >/dev/null 2>&1
            if [ $? -ne 0 ]; then
                /bin/systemctl start lwsmd
            fi
        fi
    fi

%pre client

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
        # Not in chroot
        if [ -z "`pidof lwsmd`" ]; then
            /bin/systemctl >/dev/null 2>&1
            if [ $? -ne 0 ]; then
                /bin/systemctl start lwsmd
            fi
        fi
    fi

%post

    /sbin/ldconfig

    /bin/mkdir -m 755 -p %{_logdir}
    /bin/mkdir -m 755 -p %{_logconfdir}
    if [ -a %{_logconfdir}/vmdnsd-syslog-ng.conf ]; then
        /bin/rm %{_logconfdir}/vmdnsd-syslog-ng.conf
    fi
    /bin/ln -s %{_datadir}/config/vmdnsd-syslog-ng.conf %{_logconfdir}/vmdnsd-syslog-ng.conf

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    case "$1" in
        1)
            try_starting_lwregd_svc=true

            if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
                try_starting_lwregd_svc=false
            fi

            /bin/systemctl >/dev/null 2>&1
            if [ $? -ne 0 ]; then
                try_starting_lwregd_svc=false
            fi

            if [ $try_starting_lwregd_svc = true ]; then
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdns.reg
                %{_likewise_open_bindir}/lwsm -q refresh
            else
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdns.reg
                if [ $started_lwregd = true ]; then
                    kill -TERM `pidof lwregd`
                    wait
                fi
            fi
            ;;         
        2)
            try_starting_lwregd_svc=true

            if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
                try_starting_lwregd_svc=false
            fi

            /bin/systemctl >/dev/null 2>&1
            if [ $? -ne 0 ]; then
                try_starting_lwregd_svc=false
            fi

            if [ $try_starting_lwregd_svc = true ]; then
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/vmdns.reg
                %{_likewise_open_bindir}/lwsm -q refresh
            else
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/vmdns.reg
                if [ $started_lwregd = true ]; then
                    kill -TERM `pidof lwregd`
                    wait
                fi
            fi
            ;;
    esac

%post client

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    case "$1" in
        1)
            try_starting_lwregd_svc=true

            if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
                try_starting_lwregd_svc=false
            fi

            /bin/systemctl >/dev/null 2>&1
            if [ $? -ne 0 ]; then
                try_starting_lwregd_svc=false
            fi

            if [ $try_starting_lwregd_svc = true ]; then
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdns-client.reg
                %{_likewise_open_bindir}/lwsm -q refresh
            else
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdns-client.reg
                if [ $started_lwregd = true ]; then
                    kill -TERM `pidof lwregd`
                    wait
                fi
            fi
            ;;         
        2)
            try_starting_lwregd_svc=true

            if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
                try_starting_lwregd_svc=false
            fi

            /bin/systemctl >/dev/null 2>&1
            if [ $? -ne 0 ]; then
                try_starting_lwregd_svc=false
            fi

            if [ $try_starting_lwregd_svc = true ]; then
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/vmdns-client.reg
                %{_likewise_open_bindir}/lwsm -q refresh
            else
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/vmdns-client.reg
                if [ $started_lwregd = true ]; then
                    kill -TERM `pidof lwregd`
                    wait
                fi
            fi
            ;;
    esac

%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    case "$1" in
        0)
            ;;
    esac

%preun client

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    case "$1" in
        0)
            ;;
    esac

%postun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    /sbin/ldconfig




%postun client

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade
    case "$1" in
        0)
            ;;
    esac

%files
%defattr(-,root,root)
%{_sbindir}/vmdnsd
%{_datadir}/config/vmdns.reg
%{_datadir}/config/vmdnsd-syslog-ng.conf

%files client
%defattr(-,root,root)
%{_bindir}/vmdns-cli
%{_datadir}/config/vmdns-client.reg
%{_lib64dir}/libvmdnsclient.*
%{_lib64dir}/libvmsock.*

%files client-devel
%defattr(-,root,root,0755)
%{_includedir}/vmdns.h
%{_includedir}/vmdnstypes.h
%{_lib64dir}/libvmdnsclient.*
%{_lib64dir}/libvmsock.*

%exclude %{_bindir}/dnstest

%changelog
*   Thu Mar 30 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-1
-   Initial - spec modified for Photon from lightwave git repo.
