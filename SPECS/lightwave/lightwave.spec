Name:          lightwave
Summary:       VMware Lightwave
Version:       1.3.1.7
Release:       3%{?dist}
License:       Apache 2.0
Group:         Applications/System
Vendor:        VMware, Inc.
URL: 	       https://github.com/vmware/lightwave
Source0:       lightwave-%{version}.tar.gz
Patch0:        lightwave-gssapi-unix-creds-separation.patch
Patch1:        lightwave-aarch64-support.patch
%define sha1 lightwave=abe987b67aadab05040ac38c11474b8d93fe8644
Distribution:  Photon

Requires:  apache-tomcat >= 8.5.8
Requires:  boost = 1.66.0
Requires:  commons-daemon >= 1.0.15
Requires:  (coreutils >= 8.22 or toybox)
Requires:  cyrus-sasl >= 2.1
Requires:  e2fsprogs
Requires:  gawk >= 4.1.3
Requires:  krb5 >= 1.14
Requires:  likewise-open >= 6.2.11.4
Requires:  openjre8 >= %{JAVA8_VERSION}
Requires:  openssl >= 1.0.2
Requires:  lightwave-client = %{version}

BuildRequires: ant-contrib >= 1.0
BuildRequires: apache-maven >= 3.3.9
BuildRequires: boost-devel = 1.66.0
BuildRequires: c-rest-engine-devel >= 1.1
BuildRequires: commons-daemon >= 1.0.15
BuildRequires: copenapi-devel
BuildRequires: coreutils >= 8.22
BuildRequires: curl-devel
BuildRequires: e2fsprogs-devel
BuildRequires: jansson-devel
BuildRequires: krb5-devel >= 1.14
BuildRequires: likewise-open-devel >= 6.2.10
BuildRequires: openjdk8 >= %{JAVA8_VERSION}
BuildRequires: openssl-devel >= 1.0.2
BuildRequires: python2-devel >= 2.7.8
BuildRequires: sqlite-devel >= 3.14
BuildRequires: go
BuildRequires: binutils

%description
VMware Lightwave Server

%define _jarsdir %{_prefix}/jars
%define _webappsdir %{_prefix}/vmware-sts/webapps
%define _configdir %{_datadir}/config
%define _servicedir /lib/systemd/system
%define _commons_daemon_home /usr/share/java
%define _tomcat_home /var/opt/apache-tomcat
%define _java_home /usr/lib/jvm/OpenJDK-%{JAVA8_VERSION}
%define _ant_home /var/opt/apache-ant
%define _maven_home /var/opt/apache-maven

%if 0%{?_likewise_open_prefix:1} == 0
%define _likewise_open_prefix /opt/likewise
%endif

%define _likewise_open_bindir %{_likewise_open_prefix}/bin
%define _likewise_open_sbindir %{_likewise_open_prefix}/sbin
%define _lwisbindir %{_likewise_open_bindir}

%if 0%{?_javahome:1} == 0
%define _javahome %{_java_home}
%endif

%define _sasl2dir %{_libdir}/sasl2
%define _krb5_lib_dir %{_libdir}
%define _krb5_gss_conf_dir /etc/gss
%define _logdir /var/log/lightwave
%define _logconfdir /etc/syslog-ng/lightwave.conf.d
%define _pymodulesdir /opt/vmware/site-packages/identity
%define _jreextdir /etc/alternatives/jre/lib/ext

%define _lightwavedbdir /var/lib/vmware

%define _post_dbdir   %{_lightwavedbdir}/post
%define _vmca_dbdir   %{_lightwavedbdir}/vmca
%define _vmdir_dbdir  %{_lightwavedbdir}/vmdir
%define _vmafd_dbdir  %{_lightwavedbdir}/vmafd
%define _vmsts_dbdir  %{_lightwavedbdir}/vmsts

%define _vecsdir %{_vmafd_dbdir}/vecs
%define _crlsdir %{_vmafd_dbdir}/crl

%package client-libs
Summary: Lightwave Client libs

%description client-libs
Client libraries to communicate with Lightwave Services

%package client
Summary: Lightwave Client
Requires: c-rest-engine >= 1.1
Requires: copenapi
Requires: coreutils >= 8.22
Requires: cyrus-sasl >= 2.1
Requires: openssl >= 1.0.2
Requires: jansson
Requires: krb5 >= 1.14
Requires: likewise-open >= 6.2.9
Requires: openjdk8 >= %{JAVA8_VERSION}
Requires: boost = 1.66.0
Requires: lightwave-client-libs = %{version}-%{release}

%description client
Client utils to communicate with Lightwave Services

%package devel
Summary: Lightwave Client Development Library
Requires: lightwave-client = %{version}-%{release}

%description devel
Development Libraries to communicate with Lightwave Services

%package post
Summary: Lightwave POST Service
Requires: lightwave-client = %{version}-%{release}
%description post
Lightwave POST service

%prep
%setup -qn lightwave-%{version}
%patch0 -p1
%patch1 -p1
sed -i 's|/opt/vmware/bin/certool|/usr/bin/certool|' vmidentity/install/src/main/java/com/vmware/identity/configure/LinuxInstallerHelper.java
sed -i 's/VMIDENTITY_LIB_DIR=\/opt\/vmware\/lib64/VMIDENTITY_LIB_DIR=\/usr\/jars/' vmidentity/websso/src/main/resources/sso-config.sh
sed -i 's,/opt/vmware/bin/ic-join,/usr/bin/ic-join,' config/scripts/domainjoin.sh
sed -i 's#$COMMONS_DAEMON_HOME#usr#g' configure.ac
%build

cd build
autoreconf -mif .. &&
../configure \
    CFLAGS="-Wall -Werror -Wno-unused-but-set-variable -Wno-pointer-sign -Wno-implicit-function-declaration -Wno-address -Wno-enum-compare" \
    LDFLAGS=-ldl \
    --prefix=%{_prefix} \
    --libdir=%{_lib64dir} \
    --localstatedir=%{_localstatedir}
make

%install

[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
cd build && make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/opt/vmware/share/config
find %{buildroot} -name '*.a' -delete
find %{buildroot} -name '*.la' -delete

%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    case "$1" in
        1)
            #
            # New Installation
            #
            if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
                # Not in chroot
                if [ -z "`pidof lwsmd`" ]; then
                    /bin/systemctl >/dev/null 2>&1
                    if [ $? -ne 0 ]; then
                        /bin/systemctl start lwsmd
                    fi
                fi
            fi
            ;;

        2)
            #
            # Upgrade
            #
            if [ ! -d %{_backupdir} ];
            then
                /bin/mkdir "%{_backupdir}"
            fi
            /bin/cp "%{_prefix}/vmware-sts/conf/server.xml" "%{_backupdir}/server.xml"
            ;;

    esac

%pre client

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    case "$1" in
        1)
            #
            # New Installation
            #
            /bin/systemctl >/dev/null 2>&1
            if [ $? -eq 0 ]; then
                if [ -z "`pidof lwsmd`" ]; then
                    /bin/systemctl start lwsmd
                fi
            fi
            ;;

        2)
            #
            # Upgrade
            #
            ;;
    esac

%pre post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    case "$1" in
        1)
            #
            # New Installation
            #
            /bin/systemctl >/dev/null 2>&1
            if [ $? -eq 0 ]; then
                if [ -z "`pidof lwsmd`" ]; then
                    /bin/systemctl start lwsmd
                fi
            fi
            ;;

        2)
            #
            # Upgrade
            #
            ;;
    esac

%post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    /sbin/ldconfig
#this is a hack till lightwave java paths are fixed.
if [ $1 -eq 1 ]; then
  mkdir -p /opt/vmware
  ln -sf %{_lib64dir} /opt/vmware/
  ln -sf %{_sbindir} /opt/vmware/
  ln -sf %{_jarsdir} /opt/vmware/
  ln -sf %{_prefix}/vmware-sts /opt/vmware/
fi

# config

    /bin/systemctl >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        /bin/systemctl daemon-reload
    fi

# vmdir

    /bin/mkdir -m 700 -p %{_vmdir_dbdir}

    if [ -a %{_sasl2dir}/vmdird.conf ]; then
        /bin/rm %{_sasl2dir}/vmdird.conf
    fi

    # add vmdird.conf to sasl2 directory
    /bin/ln -s %{_datadir}/config/saslvmdird.conf %{_sasl2dir}/vmdird.conf

    /bin/mkdir -m 755 -p %{_logconfdir}
    if [ -a %{_logconfdir}/vmdird-syslog-ng.conf ]; then
        /bin/rm %{_logconfdir}/vmdird-syslog-ng.conf
    fi
    /bin/ln -s %{_datadir}/config/vmdird-syslog-ng.conf %{_logconfdir}/vmdird-syslog-ng.conf

# vmdns

    /bin/mkdir -m 755 -p %{_logdir}
    /bin/mkdir -m 755 -p %{_logconfdir}
    if [ -a %{_logconfdir}/vmdnsd-syslog-ng.conf ]; then
        /bin/rm %{_logconfdir}/vmdnsd-syslog-ng.conf
    fi
    /bin/ln -s %{_datadir}/config/vmdnsd-syslog-ng.conf %{_logconfdir}/vmdnsd-syslog-ng.conf

# vmca

    /bin/mkdir -m 700 -p %{_vmca_dbdir}
    /bin/mkdir -m 755 -p %{_logdir}
    /bin/mkdir -m 755 -p %{_logconfdir}
    if [ -a %{_logconfdir}/vmcad-syslog-ng.conf ]; then
        /bin/rm %{_logconfdir}/vmcad-syslog-ng.conf
    fi
    /bin/ln -s %{_datadir}/config/vmcad-syslog-ng.conf %{_logconfdir}/vmcad-syslog-ng.conf

    case "$1" in
        1)
            #
            # New Installation
            #
            try_starting_lwregd_svc=true

            if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
                try_starting_lwregd_svc=false
            fi

            /bin/systemctl >/dev/null 2>&1
            if [ $? -ne 0 ]; then
                try_starting_lwregd_svc=false
            fi

            if [ $try_starting_lwregd_svc = true ]; then
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdir.reg
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdns.reg
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmca.reg
                %{_likewise_open_bindir}/lwsm -q refresh
                sleep 5
            else
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdir.reg
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdns.reg
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmca.reg
                if [ $started_lwregd = true ]; then
                    kill -TERM `pidof lwregd`
                    wait
                fi
            fi

        /bin/systemctl enable vmware-stsd.service >/dev/null 2>&1
        if [ $? -ne 0 ]; then
            /bin/ln -s /lib/systemd/system/vmware-stsd.service /etc/systemd/system/multi-user.target.wants/vmware-stsd.service
        fi
        /bin/systemctl >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            /bin/systemctl daemon-reload
        fi

            ;;

        2)
            #
            # Upgrade
            #

            %{_sbindir}/configure-build.sh "%{_backupdir}"

            try_starting_lwregd_svc=true

            if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
                try_starting_lwregd_svc=false
            fi

            /bin/systemctl >/dev/null 2>&1
            if [ $? -ne 0 ]; then
                try_starting_lwregd_svc=false
            fi

            if [ $try_starting_lwregd_svc = true ]; then
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/vmdir.reg
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/vmdns.reg
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/vmca.reg
                %{_likewise_open_bindir}/lwsm -q refresh
                sleep 5
            else
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdir.reg
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdns.reg
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmca.reg
                if [ $started_lwregd = true ]; then
                    kill -TERM `pidof lwregd`
                    wait
                fi
            fi
            ;;
    esac

if [ -x "%{_lwisbindir}/lwregshell" ]
then
    %{_lwisbindir}/lwregshell list_keys "[HKEY_THIS_MACHINE\Software\VMware\Identity]" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        # add key if not exist
        %{_lwisbindir}/lwregshell add_key "[HKEY_THIS_MACHINE\Software]"
        %{_lwisbindir}/lwregshell add_key "[HKEY_THIS_MACHINE\Software\VMware]"
        %{_lwisbindir}/lwregshell add_key "[HKEY_THIS_MACHINE\Software\VMware\Identity]"
    fi

    %{_lwisbindir}/lwregshell list_values "[HKEY_THIS_MACHINE\Software\VMware\Identity]" | grep "Release" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        # add value if not exist
        %{_lwisbindir}/lwregshell add_value "[HKEY_THIS_MACHINE\Software\VMware\Identity]" "Release" REG_SZ "Lightwave"
    fi

    %{_lwisbindir}/lwregshell list_values "[HKEY_THIS_MACHINE\Software\VMware\Identity]" | grep "Version" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        # add value if not exist
        %{_lwisbindir}/lwregshell add_value "[HKEY_THIS_MACHINE\Software\VMware\Identity]" "Version" REG_SZ "%{version}"
    else
        # set value if exists
        %{_lwisbindir}/lwregshell set_value "[HKEY_THIS_MACHINE\Software\VMware\Identity]" "Version" "%{version}"
    fi
fi


%post client

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    /bin/mkdir -m 755 -p %{_logdir}

    /bin/mkdir -m 700 -p %{_vmafd_dbdir}
    /bin/mkdir -m 700 -p %{_vecsdir}
    /bin/mkdir -m 700 -p %{_crlsdir}

    /bin/mkdir -m 755 -p %{_logdir}
    /bin/mkdir -m 755 -p %{_logconfdir}
    if [ -a %{_logconfdir}/vmafdd-syslog-ng.conf ]; then
        /bin/rm %{_logconfdir}/vmafdd-syslog-ng.conf
    fi
    /bin/ln -s %{_datadir}/config/vmafdd-syslog-ng.conf %{_logconfdir}/vmafdd-syslog-ng.conf

    case "$1" in
        1)
            #
            # New Installation
            #
            try_starting_lwregd_svc=true

            if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
                try_starting_lwregd_svc=false
            fi

            /bin/systemctl >/dev/null 2>&1
            if [ $? -ne 0 ]; then
                try_starting_lwregd_svc=false
            fi

            if [ $try_starting_lwregd_svc = true ]; then
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmafd.reg
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdir-client.reg
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdns-client.reg
                %{_likewise_open_bindir}/lwsm -q refresh
                sleep 5
            else
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmafd.reg
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdir-client.reg
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdns-client.reg
                if [ $started_lwregd = true ]; then
                    kill `pidof lwregd`
                    wait
                fi
            fi
            ;;

        2)
            #
            # Upgrade
            #
            try_starting_lwregd_svc=true

            if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
                try_starting_lwregd_svc=false
            fi

            /bin/systemctl >/dev/null 2>&1
            if [ $? -ne 0 ]; then
                try_starting_lwregd_svc=false
            fi

            if [ $try_starting_lwregd_svc = true ]; then
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/vmafd.reg
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/vmdir-client.reg
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/vmdns-client.reg
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmafd.reg
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdir-client.reg
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdns-client.reg
                if [ $started_lwregd = true ]; then
                    kill `pidof lwregd`
                    wait
                fi
            fi
            ;;
    esac

%post client-libs
    # add libgssapi_srp.so to GSSAPI plugin directory
    if [ ! -h %{_krb5_lib_dir}/gss/libgssapi_srp.so ]; then
        /bin/ln -s %{_lib64dir}/libgssapi_srp.so %{_krb5_lib_dir}/gss/libgssapi_srp.so
    fi

    # Add GSSAPI SRP plugin configuration to GSS mech file
    if [ -f %{_krb5_gss_conf_dir}/mech ]; then
        if [ `grep -c  "1.2.840.113554.1.2.10" %{_krb5_gss_conf_dir}/mech` -lt 1 ]; then
            echo "srp  1.2.840.113554.1.2.10 libgssapi_srp.so" >> %{_krb5_gss_conf_dir}/mech
        fi
    fi

    # Restore commented out NTLM mech oid if found
    if [ `grep -c  "#ntlm " %{_krb5_gss_conf_dir}/mech` -ge 1 ]; then
        /bin/mv %{_krb5_gss_conf_dir}/mech %{_krb5_gss_conf_dir}/mech-$$
        /bin/cat %{_krb5_gss_conf_dir}/mech-$$ | sed 's|^#ntlm|ntlm|' > %{_krb5_gss_conf_dir}/mech
        if [ -s %{_krb5_gss_conf_dir}/mech ]; then
            /bin/rm %{_krb5_gss_conf_dir}/mech-$$
        fi
    fi

%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    case "$1" in
        0)
            #
            # Uninstall
            #
            /bin/systemctl >/dev/null 2>&1
            if [ $? -eq 0 ]; then
                 if [ -f /etc/systemd/system/vmware-stsd.service ]; then
                     /bin/systemctl stop vmware-stsd.service
                     /bin/systemctl disable vmware-stsd.service
                     /bin/rm -f /etc/systemd/system/vmware-stsd.service
                     /bin/systemctl daemon-reload
                 fi
            fi

            %{_likewise_open_bindir}/lwsm info vmca > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                echo "Stopping the Certificate Authority Service..."
                %{_likewise_open_bindir}/lwsm stop vmca
                echo "Removing service configuration..."
                %{_likewise_open_bindir}/lwregshell delete_tree 'HKEY_THIS_MACHINE\Services\vmca'
                echo "Restarting service control manager..."
                /bin/systemctl restart lwsmd
                sleep 5
                echo "Autostart services..."
                %{_likewise_open_bindir}/lwsm autostart
            fi

            %{_likewise_open_bindir}/lwsm info vmdir > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                %{_likewise_open_bindir}/lwsm stop vmdir
                %{_likewise_open_bindir}/lwregshell delete_tree 'HKEY_THIS_MACHINE\Services\vmdir'
                /bin/systemctl restart lwsmd
                %{_likewise_open_bindir}/lwsm autostart
            fi

# dns also?

            /bin/systemctl >/dev/null 2>&1
            if [ $? -eq 0 ]; then
                 if [ -f /etc/systemd/system/firewall.service ]; then
                     /bin/systemctl stop firewall.service
                     /bin/systemctl disable firewall.service
                     /bin/rm -f /etc/systemd/system/firewall.service
                     /bin/systemctl daemon-reload
                 fi
            fi

            if [ -h %{_logconfdir}/vmdird-syslog-ng.conf ]; then
                /bin/rm -f %{_logconfdir}/vmdird-syslog-ng.conf
            fi
            if [ -h %{_logconfdir}/vmcad-syslog-ng.conf ]; then
                /bin/rm -f %{_logconfdir}/vmcad-syslog-ng.conf
            fi
            if [ -h %{_logconfdir}/vmdnsd-syslog-ng.conf ]; then
                /bin/rm -f %{_logconfdir}/vmdnsd-syslog-ng.conf
            fi
            ;;

        1)
            #
            # Upgrade
            #
            ;;
    esac

%preun client

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    case "$1" in
        0)
            #
            # Uninstall
            #
            %{_likewise_open_bindir}/lwsm info vmafd > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                echo "Stopping the AFD Service..."
                %{_likewise_open_bindir}/lwsm stop vmafd
                echo "Removing service configuration..."
                %{_likewise_open_bindir}/lwregshell delete_tree 'HKEY_THIS_MACHINE\Services\vmafd'
                echo "Restarting service control manager..."
                /bin/systemctl restart lwsmd
                sleep 5
                echo "Autostart services..."
                %{_likewise_open_bindir}/lwsm autostart
            fi


            if [ -h %{_logconfdir}/vmafdd-syslog-ng.conf ]; then
                /bin/rm -f %{_logconfdir}/vmafdd-syslog-ng.conf
            fi
            ;;

        1)
            #
            # Upgrade
            #
            ;;
    esac

%preun client-libs

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    case "$1" in
        0)
            #
            # Uninstall
            #
            # Cleanup GSSAPI SRP symlink
            if [ -h %{_krb5_lib_dir}/gss/libgssapi_srp.so ]; then
                /bin/rm -f %{_krb5_lib_dir}/gss/libgssapi_srp.so
            fi

            # Remove GSSAPI SRP Plugin configuration from GSS mech file
            if [ -f %{_krb5_gss_conf_dir}/mech ]; then
                if [ `grep -c "1.2.840.113554.1.2.10" %{_krb5_gss_conf_dir}/mech` -gt 0 ]; then
                    /bin/cat %{_krb5_gss_conf_dir}/mech | sed '/1.2.840.113554.1.2.10/d' > "/tmp/mech-$$"
                    if [ -s /tmp/mech-$$ ]; then
                        /bin/mv "/tmp/mech-$$" %{_krb5_gss_conf_dir}/mech
                    fi
                fi
            fi
            ;;

        1)
            #
            # Upgrade
            #
            ;;
    esac

%postun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    /sbin/ldconfig

    case "$1" in
        0)
            #
            # Uninstall
            #
            echo "Existing database files kept at [%{_vmdir_dbdir}]."

            if [ -x "%{_lwisbindir}/lwregshell" ]
            then
                %{_lwisbindir}/lwregshell list_keys "[HKEY_THIS_MACHINE\Software\VMware\Identity]" > /dev/null 2>&1
                if [ $? -eq 0 ]; then
                    # delete key if exist
                    %{_lwisbindir}/lwregshell delete_tree "[HKEY_THIS_MACHINE\Software\VMware\Identity]"
                fi
            fi
            ;;

        1)
            #
            # Upgrade
            #
            ;;
    esac

    if [ -a %{_sasl2dir}/vmdird.conf ]; then
        /bin/rm %{_sasl2dir}/vmdird.conf
    fi

%postun client

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    /sbin/ldconfig

    case "$1" in
        0)
            #
            # Uninstall
            #
            echo "Existing VECS files kept under [%{_vmafd_dbdir}]"
            ;;

        1)
            #
            # Upgrade
            #
            ;;
    esac


%post post

    /bin/mkdir -m 700 -p %{_post_dbdir}

    if [ -a %{_sasl2dir}/postd.conf ]; then
        /bin/rm %{_sasl2dir}/postd.conf
    fi

    # add postd.conf to sasl2 directory
    /bin/ln -s %{_datadir}/config/saslpostd.conf %{_sasl2dir}/postd.conf

    /bin/mkdir -m 755 -p %{_logdir}
    /bin/mkdir -m 755 -p %{_logconfdir}
    if [ -a %{_logconfdir}/postd-syslog-ng.conf ]; then
        /bin/rm %{_logconfdir}/postd-syslog-ng.conf
    fi
    /bin/ln -s %{_datadir}/config/postd-syslog-ng.conf %{_logconfdir}/postd-syslog-ng.conf

    case "$1" in
        1)
            #
            # New Installation
            #
            try_starting_lwregd_svc=true

            if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
                try_starting_lwregd_svc=false
            fi

            /bin/systemctl >/dev/null 2>&1
            if [ $? -ne 0 ]; then
                try_starting_lwregd_svc=false
            fi

            if [ $try_starting_lwregd_svc = true ]; then
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/post.reg
                %{_likewise_open_bindir}/lwsm -q refresh
                sleep 5
            else
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/post.reg
                if [ $started_lwregd = true ]; then
                    kill -TERM `pidof lwregd`
                    wait
                fi
            fi
            ;;

        2)
            #
            # Upgrade
            #
            try_starting_lwregd_svc=true

            if [ "$(stat -c %d:%i /)" != "$(stat -c %d:%i /proc/1/root/.)" ]; then
                try_starting_lwregd_svc=false
            fi

            /bin/systemctl >/dev/null 2>&1
            if [ $? -ne 0 ]; then
                try_starting_lwregd_svc=false
            fi

            if [ $try_starting_lwregd_svc = true ]; then
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/post.reg
                %{_likewise_open_bindir}/lwsm -q refresh
                sleep 5
            else
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/post.reg
                if [ $started_lwregd = true ]; then
                    kill -TERM `pidof lwregd`
                    wait
                fi
            fi
            ;;
    esac

%preun post

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    case "$1" in
        0)
            #
            # Uninstall
            #
            %{_likewise_open_bindir}/lwsm info post > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                %{_likewise_open_bindir}/lwsm stop post
                %{_likewise_open_bindir}/lwregshell delete_tree 'HKEY_THIS_MACHINE\Services\post'
                /bin/systemctl restart lwsmd
                sleep 5
            fi
            ;;

        1)
            #
            # Upgrade
            #
            ;;
    esac


%postun post

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    /sbin/ldconfig

    case "$1" in
        0)
            #
            # Uninstall
            #
            echo "Existing database files kept at [%{_post_dbdir}]."
            ;;

        1)
            #
            # Upgrade
            #
            ;;
    esac

    if [ -a %{_sasl2dir}/postd.conf ]; then
        /bin/rm %{_sasl2dir}/postd.conf
    fi

%files

%defattr(-,root,root,0755)
%dir /opt/vmware/share/config
%{_bindir}/configure-sts
%{_bindir}/ic-promote
%{_bindir}/configure-lightwave-server
%{_bindir}/configure-identity-server
%{_bindir}/test-ldapbind
%{_bindir}/test-logon
%{_bindir}/test-svr
%{_bindir}/vdcadmintool
%{_bindir}/vdcbackup
%{_bindir}/vdcleavefed
%{_bindir}/vdcpass
%{_bindir}/vdcrepadmin
%{_bindir}/vdcsetupldu
%{_bindir}/vdcsrp
%{_bindir}/unix_srp
%{_bindir}/vdcupgrade
%{_bindir}/vmkdc_admin
%{_bindir}/vdcmetric
%{_bindir}/vdcschema
%{_bindir}/vmdir_upgrade.sh
%{_bindir}/vdcresetMachineActCred

%{_sbindir}/vmcad
%{_sbindir}/vmdird
%{_sbindir}/vmdnsd
%{_sbindir}/vmware-stsd.sh
%{_sbindir}/configure-build.sh
%{_sbindir}/sso-config.sh

%{_lib64dir}/sasl2/libsaslvmdirdb.so*

%{_datadir}/config/vmca.reg
%{_datadir}/config/vmcad-syslog-ng.conf
%{_datadir}/config/saslvmdird.conf
%{_datadir}/config/vmdir.reg
%{_datadir}/config/vmdirschema.ldif
%{_datadir}/config/vmdird-syslog-ng.conf
%{_datadir}/config/vmdir-rest.json
%{_datadir}/config/vmdns.reg
%{_datadir}/config/vmdns-rest.json
%{_datadir}/config/vmdnsd-syslog-ng.conf
%{_datadir}/config/idm/*
%{_datadir}/config/vmca-telegraf.conf
%{_datadir}/config/vmdir-telegraf.conf
%{_datadir}/config/vmdns-telegraf.conf

%{_jarsdir}/openidconnect-client-lib.jar
%{_jarsdir}/openidconnect-common.jar
%{_jarsdir}/openidconnect-protocol.jar
%{_jarsdir}/samlauthority.jar
%{_jarsdir}/vmware-identity-diagnostics.jar
%{_jarsdir}/vmware-identity-idm-server.jar
%{_jarsdir}/vmware-identity-rest-afd-server.jar
%{_jarsdir}/vmware-identity-rest-core-server.jar
%{_jarsdir}/vmware-identity-rest-idm-server.jar
%{_jarsdir}/vmware-directory-rest-server.jar
%{_jarsdir}/vmware-identity-install.jar
%{_jarsdir}/vmware-identity-sso-config.jar
%{_jarsdir}/websso.jar
%{_jarsdir}/sts.jar
%{_jarsdir}/openidconnect-server.jar
%{_jarsdir}/commons-lang-2.6.jar
%{_jarsdir}/commons-logging-1.2.jar
%{_jarsdir}/jna-4.2.1.jar
%{_jarsdir}/httpclient-4.5.1.jar
%{_jarsdir}/slf4j-api-1.7.25.jar
%{_jarsdir}/log4j-api-2.8.2.jar
%{_jarsdir}/log4j-slf4j-impl-2.8.2.jar
%{_jarsdir}/log4j-core-2.8.2.jar
%{_jarsdir}/args4j-2.33.jar
%{_jarsdir}/commons-codec-1.9.jar
%{_jarsdir}/commons-lang3-3.3.2.jar
%{_jarsdir}/httpcore-4.4.4.jar
%{_jarsdir}/jackson-annotations-2.8.4.jar
%{_jarsdir}/jackson-core-2.8.4.jar
%{_jarsdir}/jackson-databind-2.8.4.jar
%{_jarsdir}/jersey-media-json-jackson-2.25.1.jar
%{_jarsdir}/json-smart-1.3.1.jar
%{_jarsdir}/nimbus-jose-jwt-4.12.jar


%{_webappsdir}/lightwaveui.war
%{_webappsdir}/ROOT.war

%{_configdir}/setfirewallrules.py
%{_configdir}/lw-firewall-server.json

%{_servicedir}/firewall.service
%{_servicedir}/vmware-stsd.service

%config %attr(600, root, root) %{_prefix}/vmware-sts/bin/setenv.sh
%config %attr(600, root, root) %{_prefix}/vmware-sts/bin/vmware-identity-tomcat-extensions.jar
%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/catalina.policy
%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/catalina.properties
%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/context.xml
%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/logging.properties
%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/server.xml
%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/web.xml
%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/tomcat-users.xml
%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/vmsts-telegraf.conf

%files client-libs
%{_lib64dir}/libvmafcfgapi.so*
%{_lib64dir}/libvmafdclient.so*
%{_lib64dir}/libvmeventclient.so*
%{_lib64dir}/libvmcaclient.so*
%{_lib64dir}/libvmdirclient.so*
%{_lib64dir}/libkrb5crypto.so*
%{_lib64dir}/libvmkdcserv.so*
%{_lib64dir}/libcsrp.so*
%{_lib64dir}/libgssapi_ntlm.so*
%{_lib64dir}/libgssapi_srp.so*
%{_lib64dir}/libgssapi_unix.so*
%{_lib64dir}/libgssapi_unix_creds.so*
%{_lib64dir}/libvmdnsclient.so*
%{_lib64dir}/libcfgutils.so*


%files client

%defattr(-,root,root)

%{_bindir}/ic-join
%{_bindir}/cdc-cli
%{_bindir}/certool
%{_bindir}/dir-cli
%{_bindir}/domainjoin
%{_bindir}/domainjoin.sh
%{_bindir}/lw-support-bundle.sh
%{_bindir}/sl-cli
%{_bindir}/vmafd-cli
%{_bindir}/vmdns-cli
%{_bindir}/vdcaclmgr
%{_bindir}/vdcpromo
%{_bindir}/vecs-cli

%{_sbindir}/vmafdd

%{_lib64dir}/libvecsjni.so*
%{_lib64dir}/libcdcjni.so*
%{_lib64dir}/libheartbeatjni.so*
%{_lib64dir}/libidm.so*
%{_lib64dir}/libpostclient.so*
%{_lib64dir}/libssoafdclient.so*
%{_lib64dir}/libssocommon.so*
%{_lib64dir}/libssocoreclient.so*
%{_lib64dir}/libssoidmclient.so*
%{_lib64dir}/libssooidc.so*
%{_lib64dir}/libssovmdirclient.so*
%{_lib64dir}/libvmdirauth.so*
%{_lib64dir}/libvmmetrics.so*

%{_datadir}/config/java.security.linux
%{_datadir}/config/certool.cfg
%{_datadir}/config/vmafd.reg
%{_datadir}/config/vmdir-client.reg
%{_datadir}/config/vmdns-client.reg
%{_datadir}/config/vmafdd-syslog-ng.conf
%{_datadir}/config/lw-firewall-client.json
%{_datadir}/config/refresh-resolve-conf.sh
%{_datadir}/config/telegraf.conf
%{_datadir}/config/vmafd-telegraf.conf


%{_jreextdir}/vmware-endpoint-certificate-store.jar
%{_jreextdir}/client-domain-controller-cache.jar
%{_jreextdir}/afd-heartbeat-service.jar

%{_jarsdir}/authentication-framework.jar
%{_jarsdir}/vmware-identity-rest-idm-samples.jar
%{_jarsdir}/vmware-vmca-client.jar
%{_jarsdir}/samltoken.jar
%{_jarsdir}/vmware-identity-rest-idm-common.jar
%{_jarsdir}/vmware-directory-rest-common.jar
%{_jarsdir}/vmware-directory-rest-client.jar
%{_jarsdir}/vmware-identity-rest-core-common.jar
%{_jarsdir}/vmware-identity-websso-client.jar
%{_jarsdir}/vmware-identity-platform.jar
%{_jarsdir}/vmware-identity-wsTrustClient.jar
%{_jarsdir}/vmware-identity-rest-afd-common.jar
%{_jarsdir}/openidconnect-common.jar
%{_jarsdir}/openidconnect-client-lib.jar
%{_jarsdir}/vmware-identity-idm-client.jar
%{_jarsdir}/vmware-identity-idm-interface.jar
%{_jarsdir}/vmware-identity-rest-afd-client.jar
%{_jarsdir}/vmware-identity-rest-core-client.jar
%{_jarsdir}/vmware-identity-rest-idm-client.jar

%{_sysconfdir}/vmware/java/vmware-override-java.security


%files devel

%defattr(-,root,root)

%{_includedir}/vmafd.h
%{_includedir}/vmafdtypes.h
%{_includedir}/vmafdclient.h
%{_includedir}/vecsclient.h
%{_includedir}/cdcclient.h
%{_includedir}/vmsuperlogging.h
%{_includedir}/vmca.h
%{_includedir}/vmcatypes.h
%{_includedir}/vmdir.h
%{_includedir}/vmdirauth.h
%{_includedir}/vmdirclient.h
%{_includedir}/vmdirerrors.h
%{_includedir}/vmdirtypes.h
%{_includedir}/vmdns.h
%{_includedir}/vmdnstypes.h
%{_includedir}/vmmetrics.h
%{_includedir}/gssapi_creds_plugin.h

# TBD - not sure if these should be included or excluded
#
%{_includedir}/oidc.h
%{_includedir}/oidc_types.h
%{_includedir}/ssoafdclient.h
%{_includedir}/ssocoreclient.h
%{_includedir}/ssoerrors.h
%{_includedir}/ssoidmclient.h
%{_includedir}/ssotypes.h
%{_includedir}/ssocommon.h
%{_includedir}/ssovmdirclient.h
%{_includedir}/vmevent.h

%exclude %{_bindir}/vdcvmdirpromo
%exclude %{_bindir}/vmdirclienttest
%exclude %{_bindir}/*test

%exclude %{_lib64dir}/libcommonunittests.*
%exclude %{_lib64dir}/libmisctests.*
%exclude %{_lib64dir}/libmultitenancytests.*
%exclude %{_lib64dir}/libpasswordapistests.*
%exclude %{_lib64dir}/libsearchtests.*
%exclude %{_lib64dir}/libsecuritydescriptortests.*

%exclude %{_prefix}/site-packages/identity/*
%exclude %{_webappsdir}/openidconnect-sample-rp.war

%files post

%defattr(-,root,root)

%{_sbindir}/postd

%{_bindir}/postadmintool
%{_bindir}/lwraftpromo
%{_bindir}/postschema
%{_bindir}/post-cli
%{_bindir}/postaclmgr

%{_lib64dir}/sasl2/libsaslpostdb.so*

%{_datadir}/config/saslpostd.conf
%{_datadir}/config/postschema.ldif
%{_datadir}/config/post-rest.json
%{_datadir}/config/post.reg
%{_datadir}/config/postd-syslog-ng.conf
%{_datadir}/config/post-client.reg
%{_datadir}/config/lw-firewall-post.json
%{_datadir}/config/post-demote-deads.sh
%{_datadir}/config/post-telegraf.conf

# %doc ChangeLog README COPYING

%changelog
*   Tue Sep 18 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.3.1.7-3
-   Use boost version 1.66.0
*   Tue Dec 26 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.1.7-2
-   Aarch64 support
*   Thu Nov 23 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.3.1.7-1
-   update to lightwave 1.3.1.7 (release 1.3.1-7 in lightwave repo)
*   Mon Sep 25 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.1-5
-   Requires coreutils or toybox
*   Fri Sep 22 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.3.1-4
-   Patch for unix gsssapi creds separation
*   Tue Aug 22 2017 Rui Gu <ruig@vmware.com> 1.3.1-3
-   Add 'go' to BuildRequires
*   Thu Aug 17 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.3.1-2
-   Fix version requirement for lightwave-post
*   Wed Aug 9 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.3.1-1
-   update to 1.3.1
*   Tue Jul 18 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.1-5
-   making sure client-libs install gss mechs
-   make sure domainjoin works with just client installed.
*   Mon Jul 10 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.2.1-4
-   Updated the commons-daemon directory path to its new location
*   Tue Jun 20 2017 Divya Thaluru <dthaluru@vmware.com> 1.2.1-3
-   Fixed apache-maven directory path
*   Tue Jun 06 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.1-3
-   fix domainjoin and allow publish of oidc xml
*   Thu Jun 01 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.2.1-2
-   disable java macros and use java alternatives
*   Mon May 22 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.1-1
-   Initial - spec modified for Photon from lightwave git repo.
