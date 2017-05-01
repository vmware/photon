Name:          vmware-directory
Summary:       Directory Service
Version:       1.2.0
Release:       1%{?dist}
License:       Apache 2.0
Group:         Applications/System
Vendor:        VMware, Inc.
URL: 	       https://github.com/vmware/lightwave
Source0:       lightwave-%{version}.tar.gz
%define sha1 lightwave=5f8bb80732e5f03df321c52bf12c305e65ad66a3
Patch0:        compile-fixes.patch
Distribution:  Photon
Requires:  coreutils >= 8.22, openssl >= 1.0.2, krb5 >= 1.14, cyrus-sasl >= 2.1
Requires:  likewise-open >= 6.2.11
Requires:  vmware-directory-client = %{version}-%{release}
BuildRequires:  coreutils >= 8.22, openssl-devel >= 1.0.2, 
BuildRequires:  krb5-devel >= 1.14
BuildRequires:  cyrus-sasl >= 2.1
BuildRequires:  likewise-open-devel >= 6.2.11
BuildRequires:  vmware-event-devel >= %{version}
BuildRequires:  e2fsprogs-devel

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

%if 0%{?_vmevent_prefix:1} == 0
%define _vmevent_prefix /opt/vmware
%endif

%define _dbdir %{_localstatedir}/lib/vmware/vmdir
%define _sasl2dir %{_sasl_prefix}/lib64/sasl2
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
VMware Directory Service

%package client
Summary: VMware Directory Client
Requires:  coreutils >= 8.22, openssl >= 1.0.2, krb5 >= 1.14, cyrus-sasl >= 2.1, likewise-open >= 6.2.11
%description client
Client libraries to communicate with Directory Service

%package client-devel
Summary: VMware Directory Client Development Library
Requires: vmware-directory-client = %{version}
%description client-devel
Development Libraries to communicate with Directory Service

%prep
%setup -qn lightwave-%{version}
%patch0 -p1

%build

export CFLAGS="-Wno-unused-but-set-variable -Wno-pointer-sign -Wno-implicit-function-declaration -Wno-address -Wno-enum-compare -Wno-misleading-indentation -Wno-unused-const-variable"
cd vmdir/build
autoreconf -mif ..
../configure \
    --prefix=%{_prefix} \
    --libdir=%{_lib64dir} \
    --localstatedir=%{_localstatedir}/lib/vmware/vmdir \
    --with-likewise=%{_likewise_open_prefix} \
    --with-ssl=/usr \
    --with-sasl=%{_sasl_prefix} \
    --with-datastore=mdb \
    --with-vmevent=%{_vmevent_prefix} \
    --enable-server=yes \
    --with-version=%{version}

make

%install

[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
cd vmdir/build && make install DESTDIR=$RPM_BUILD_ROOT

%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    /bin/systemctl >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        if [ -z "`pidof lwsmd`" ]; then
            /bin/systemctl start lwsmd
        fi
    fi

%pre client

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

    if [ -a %{_sasl2dir}/vmdird.conf ]; then
        /bin/rm %{_sasl2dir}/vmdird.conf
    fi

    # add vmdird.conf to sasl2 directory
    /bin/ln -s %{_datadir}/config/saslvmdird.conf %{_sasl2dir}/vmdird.conf

    /bin/mkdir -m 755 -p %{_logdir}
    /bin/mkdir -m 755 -p %{_logconfdir}
    if [ -a %{_logconfdir}/vmdird-syslog-ng.conf ]; then
        /bin/rm %{_logconfdir}/vmdird-syslog-ng.conf
    fi
    /bin/ln -s %{_datadir}/config/vmdird-syslog-ng.conf %{_logconfdir}/vmdird-syslog-ng.conf

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
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdir.reg
                %{_likewise_open_bindir}/lwsm -q refresh
                sleep 2
            else
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdir.reg
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
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/vmdir.reg
                %{_likewise_open_bindir}/lwsm -q refresh
                sleep 2
            else
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdir.reg
                if [ $started_lwregd = true ]; then
                    kill -TERM `pidof lwregd`
                    wait
                fi
            fi
            ;;
    esac

%post client

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
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdir-client.reg
            else
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdir-client.reg
                if [ $started_lwregd = true ]; then
                    kill `pidof lwregd`
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
                %{_likewise_open_bindir}/lwregshell upgrade %{_datadir}/config/vmdir-client.reg
                started_lwregd=false
                if [ -z "`pidof lwregd`" ]; then
                    echo "Starting lwregd"
                    %{_likewise_open_sbindir}/lwregd &
                    started_lwregd=true
                    sleep 5
                fi
                %{_likewise_open_bindir}/lwregshell import %{_datadir}/config/vmdir-client.reg
                if [ $started_lwregd = true ]; then
                    kill `pidof lwregd`
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
            %{_likewise_open_bindir}/lwsm info vmdir > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                %{_likewise_open_bindir}/lwsm stop vmdir
                %{_likewise_open_bindir}/lwregshell delete_tree 'HKEY_THIS_MACHINE\Services\vmdir'
                /bin/systemctl restart lwsmd
                %{_likewise_open_bindir}/lwsm autostart
            fi

            ;;
    esac

%preun client

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    case "$1" in
        0)
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
    esac

%postun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    /sbin/ldconfig

    if [ -a %{_sasl2dir}/vmdird.conf ]; then
        /bin/rm %{_sasl2dir}/vmdird.conf
    fi

    if [ "$1" = "0" ]; then
        echo "Existing database files kept at [%{_dbdir}]."
    fi

%postun client

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade
#    case "$1" in
#        0)
#            %{_likewise_open_bindir}/lwregshell delete_tree 'HKEY_THIS_MACHINE\Services\vmdir'
#            ;;
#    esac

%files
%defattr(-,root,root)
%{_sbindir}/*
%{_bindir}/vdcadmintool
%{_bindir}/vdcbackup
%{_bindir}/vdcaclmgr
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
%{_lib64dir}/libkrb5crypto.so*
%{_lib64dir}/sasl2/libsaslvmdirdb.so*
%{_lib64dir}/libvmkdcserv.so*
%{_datadir}/config/saslvmdird.conf
%{_datadir}/config/vmdir.reg
%{_datadir}/config/vmdirschema.ldif
%{_datadir}/config/vmdird-syslog-ng.conf
%{_datadir}/config/vmdir-rest.json

%files client
%defattr(-,root,root)
%{_datadir}/config/vmdir-client.reg
%{_lib64dir}/libvmdirclient.so*
%{_lib64dir}/libcsrp.so*
%{_lib64dir}/libgssapi_ntlm.so*
%{_lib64dir}/libgssapi_srp.so*
%{_lib64dir}/libgssapi_unix.so*

%files client-devel
%defattr(-,root,root)
%{_includedir}/vmdir.h
%{_includedir}/vmdirauth.h
%{_includedir}/vmdirclient.h
%{_includedir}/vmdirerrors.h
%{_includedir}/vmdirtypes.h
%{_lib64dir}/libvmdirclient.a
%{_lib64dir}/libvmdirclient.la
%{_lib64dir}/libcsrp.a
%{_lib64dir}/libcsrp.la
%{_lib64dir}/libgssapi_ntlm.a
%{_lib64dir}/libgssapi_ntlm.la
%{_lib64dir}/libgssapi_srp.a
%{_lib64dir}/libgssapi_srp.la
%{_lib64dir}/libgssapi_unix.a
%{_lib64dir}/libgssapi_unix.la

%exclude %{_bindir}/vdcpromo
%exclude %{_bindir}/vmdirclienttest
%exclude %{_lib64dir}/libkrb5crypto.a
%exclude %{_lib64dir}/libkrb5crypto.la
%exclude %{_lib64dir}/sasl2/libsaslvmdirdb.a
%exclude %{_lib64dir}/sasl2/libsaslvmdirdb.la
%exclude %{_lib64dir}/libvmkdcserv.a
%exclude %{_lib64dir}/libvmkdcserv.la
%exclude %{_lib64dir}/*tests.*

# %doc ChangeLog README COPYING

%changelog
*   Thu Mar 30 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-1
-   Initial - spec modified for Photon from lightwave git repo.
