Name:          vmware-ca
Summary:       VMware Certificate Authority Service
Version:       1.2.0
Release:       2%{?dist}
License:       Apache 2.0
Group:         Applications/System
Vendor:        VMware, Inc.
URL: 	       https://github.com/vmware/lightwave
Source0:       lightwave-%{version}.tar.gz
%define sha1 lightwave=5f8bb80732e5f03df321c52bf12c305e65ad66a3
Distribution:  Photon
Requires:  coreutils >= 8.22, openssl >= 1.0.2, krb5 >= 1.14, cyrus-sasl >= 2.1, likewise-open >= 6.2.11, vmware-directory-client = %{version}, vmware-afd-client = %{version}, boost = 1.63.0
BuildRequires:  chkconfig
BuildRequires:  boost-devel = 1.63.0
BuildRequires:  coreutils >= 8.22
BuildRequires:  e2fsprogs-devel
BuildRequires:  openssl-devel >= 1.0.2
BuildRequires:  krb5-devel >= 1.14
BuildRequires:  cyrus-sasl >= 2.1
BuildRequires:  likewise-open-devel >= 6.2.11
BuildRequires:  openjdk8 >= 1.8.0.112-2, apache-ant >= 1.9.6-6
BuildRequires:  ant-contrib >= 1.0b3
BuildRequires:  vmware-directory-client-devel = %{version}
BuildRequires:  vmware-afd-client-devel = %{version}
BuildRequires:  sqlite-devel

%define _prefix /opt/vmware
%define _includedir %{_prefix}/include
%define _lib64dir %{_prefix}/lib64
%define _bindir %{_prefix}/bin
%define _sbindir %{_prefix}/sbin
%define _datadir %{_prefix}/share

%define _dbdir %_localstatedir/lib/vmware/vmca
%define _jarsdir %{_prefix}/jars
%define _logdir /var/log/lightwave
%define _logconfdir /etc/syslog-ng/lightwave.conf.d

%if 0%{?_likewise_open_prefix:1} == 0
%define _likewise_open_prefix /opt/likewise
%endif

%define _likewise_open_bindir %{_likewise_open_prefix}/bin
%define _likewise_open_sbindir %{_likewise_open_prefix}/sbin

%if 0%{?_vmdir_prefix:1} == 0
%define _vmdir_prefix /opt/vmware
%endif

%if 0%{?_vmafd_prefix:1} == 0
%define _vmafd_prefix /opt/vmware
%endif

%description
VMware Certificate Authority

%package client
Summary: VMware Certificate Authority Client
Requires:  coreutils >= 8.22, openssl >= 1.0.2, krb5 >= 1.14, cyrus-sasl >= 2.1, likewise-open >= 6.2.11, vmware-directory-client >= 1.2.0, vmware-afd-client >= 1.2.0
Requires: boost = 1.63.0
%description client
Client libraries to communicate with VMware Certificate Authority

%package client-devel
Summary: VMware Certificate Authority Client Development Library
Requires: vmware-ca-client = %{version}
%description client-devel
Development Libraries to communicate with VMware Certificate Authority Service

%prep
%setup -qn lightwave-%{version}

%build

export CFLAGS="-Wno-pointer-sign -Wno-unused-but-set-variable -Wno-implicit-function-declaration"
cd vmca/build
autoreconf -mif .. &&
../configure --prefix=%{_prefix}  \
            --libdir=%{_lib64dir} \
            --localstatedir=/var/lib/vmware/vmca \
            --with-java=%{_java_home} \
            --with-ant=%{_ant_home} \
            --with-likewise=%{_likewise_open_prefix} \
            --with-vmdir=%{_vmdir_prefix} \
            --with-afd=%{_vmafd_prefix} \
            --with-ssl=/usr \
            --with-boost=/usr

%install

[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
cd vmca/build && make install DESTDIR=%{buildroot}

%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    /bin/systemctl >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        if [ -z "`pidof lwsmd`" ]; then
            /bin/systemctl start lwsmd
        fi
    fi

%post

    /sbin/ldconfig

    /bin/mkdir -m 700 -p %{_dbdir}

    /bin/mkdir -m 755 -p %{_logdir}
    /bin/mkdir -m 755 -p %{_logconfdir}
    if [ -a %{_logconfdir}/vmcad-syslog-ng.conf ]; then
        /bin/rm %{_logconfdir}/vmcad-syslog-ng.conf
    fi
    /bin/ln -s %{_datadir}/config/vmcad-syslog-ng.conf %{_logconfdir}/vmcad-syslog-ng.conf

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
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmca.reg
                %{_likewise_open_bindir}/lwsm -q refresh
            else
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmca.reg
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
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/vmca.reg
                %{_likewise_open_bindir}/lwsm -q refresh
            else
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmca.reg
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
            %{_likewise_open_bindir}/lwsm info vmca > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                echo "Stopping the Certificate Authority Service..."
                %{_likewise_open_bindir}/lwsm stop vmca
                echo "Removing service configuration..."
                %{_likewise_open_bindir}/lwregshell delete_tree 'HKEY_THIS_MACHINE\Services\vmca'
                echo "Restarting service control manager..."
                /bin/systemctl restart lwsmd
                sleep 2
                echo "Autostart services..."
                %{_likewise_open_bindir}/lwsm autostart
            fi
            ;;
    esac

%postun

    /sbin/ldconfig

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    case "$1" in
        0)
            /bin/rm -rf %{_dbdir}
            ;;
    esac

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_datadir}/config/vmca.reg
%{_datadir}/config/vmcad-syslog-ng.conf

%files client
%defattr(-,root,root)
%{_bindir}/certool
%{_datadir}/config/certool.cfg
%{_lib64dir}/libvmcaclient.so
%{_lib64dir}/libvmcaclient.so.0
%{_lib64dir}/libvmcaclient.so.0.0.0
%{_jarsdir}/*.jar

%files client-devel
%defattr(-,root,root)
%{_includedir}/vmca.h
%{_includedir}/vmcatypes.h
%{_lib64dir}/libvmcaclient.a
%{_lib64dir}/libvmcaclient.la

%clean

rm -rf $RPM_BUILD_ROOT

# %doc ChangeLog README COPYING

%changelog
*	Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.2.0-2
-	Renamed openjdk to openjdk8
*   Thu Mar 30 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-1
-   Initial - spec modified for Photon from lightwave git repo.
