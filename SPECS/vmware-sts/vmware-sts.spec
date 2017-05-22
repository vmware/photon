Name:          vmware-sts
Summary:       VMware Secure Token Service
Version:       1.2.0
Release:       2%{?dist}
License:       Apache 2.0
Group:         Applications/System
Vendor:        VMware, Inc.
URL: 	       https://github.com/vmware/lightwave
Distribution:  Photon
Source0:       lightwave-%{version}.tar.gz
%define sha1 lightwave=5f8bb80732e5f03df321c52bf12c305e65ad66a3

Requires:  commons-daemon >= 1.0.15
Requires:  coreutils >= 8.22
Requires:  openssl >= 1.0.2
Requires:  likewise-open >= 6.2.11
Requires:  vmware-directory = %{version}
Requires:  vmware-afd = %{version}
Requires:  vmware-ca = %{version}
Requires:  openjre8 >= 1.8.0.112-2
Requires:  apache-tomcat >= 8.5.8
Requires:  %{name}-client = %{version}-%{release}

BuildRequires:  chkconfig
BuildRequires:  curl-devel
BuildRequires:  commons-daemon >= 1.0.15
BuildRequires:  coreutils >= 8.22
BuildRequires:  e2fsprogs-devel
BuildRequires:  jansson-devel
BuildRequires:  jaxws-ri = 2.2.10
BuildRequires:  krb5-devel >= 1.14
BuildRequires:  openssl-devel >= 1.0.2
BuildRequires:  likewise-open-devel >= 6.2.11
BuildRequires:  vmware-directory-client-devel = %{version}
BuildRequires:  vmware-ca-client-devel = %{version}
BuildRequires:  vmware-afd-client-devel = %{version}
BuildRequires:  openjdk8 >= 1.8.0.112-2, apache-ant >= 1.9.6-6
BuildRequires:  ant-contrib >= 1.0b3
BuildRequires:  apache-maven >= 3.3.9-8

%define _ant_home /var/opt/apache-ant-%{ANT_VERSION}
%define _java_home /usr/lib/jvm/OpenJDK-%{JAVA8_VERSION}
%define _maven_home /var/opt/apache-maven-%{MAVEN_VERSION}
%define _prefix /opt/vmware
%define _includedir %{_prefix}/include
%define _lib64dir %{_prefix}/lib64
%define _bindir %{_prefix}/bin
%define _sbindir %{_prefix}/sbin
%define _datadir %{_prefix}/share
%define _jreextdir %{_java_home}/jre/lib/ext

%define _dbdir %_localstatedir/lib/vmware/vmsts
%define _jarsdir %_prefix/jars
%define _binsdir %_prefix/bin
%define _webappsdir %_prefix/vmware-sts/webapps
%define _backupdir /tmp/sso
%define _commons_daemon_home /var/opt/commons-daemon-1.0.15
%define _tomcat_home /var/opt/apache-tomcat-8.0.37
%define _jaxws_home /opt/jaxws-ri-2.2.10

%if 0%{?_likewise_open_prefix:1} == 0
%define _likewise_open_prefix /opt/likewise
%endif

%define _likewise_open_bindir %{_likewise_open_prefix}/bin
%define _likewise_open_sbindir %{_likewise_open_prefix}/sbin

%description
VMware Secure Token Server

%package client
Summary:   VMware Secure Token Service Client
Requires:  coreutils >= 8.22
Requires:  openssl >= 1.0.2
Requires:  openjre8 >= 1.8.0.112-2
Requires:  vmware-directory-client >= %{version}
Requires:  likewise-open >= 6.2.11
%description client
Client libraries to communicate with VMware Secure Token Service

%package samples
Summary: VMware Secure Token Service Samples
Requires:  vmware-sts-client >= %{version}
%description samples
Samples for VMware Secure Token Service

%prep
%setup -qn lightwave-%{version}

%build
export ANT_HOME=%{_ant_home}
export PATH=$PATH:$ANT_HOME}/bin
mkdir -p vmafd/build/authentication-framework/packages/
ln -s %{_jreextdir}/*.jar vmafd/build/authentication-framework/packages/
ln -s %{_prefix}/jars/authentication-framework.jar vmafd/build/authentication-framework/packages/
mkdir -p vmca/build/packages/
ln -s %{_prefix}/jars/vmware-vmca-client.jar vmca/build/packages/
cd vmidentity/build
autoreconf -mif .. &&
../configure --prefix=%{_prefix} \
             --libdir=%{_lib64dir} \
             --localstatedir=%{_dbdir} \
             --with-afd=%{_prefix} \
             --with-likewise=%{_likewise_open_prefix} \
             --with-jansson=/usr \
             --with-curl=/usr \
             --with-ssl=/usr \
             --with-java=%{_java_home} \
             --with-commons-daemon=%{_commons_daemon_home} \
             --with-ant=%{_ant_home} \
             --with-tomcat=%{_tomcat_home} \
             --with-jax-ws=%{_jaxws_home} \
             --with-maven=%{_maven_home} \
             --disable-static
make

%install
export ANT_HOME=%{_ant_home}
export PATH=$PATH:$ANT_HOME}/bin
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
cd vmidentity/build && make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete

%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade
if [[ $1 -gt 1 ]]
then
    if [ ! -d %{_backupdir} ];
    then
        /bin/mkdir "%{_backupdir}"
    fi
    /bin/cp "%{_prefix}/vmware-sts/conf/server.xml" "%{_backupdir}/server.xml"
fi

%post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade
    /sbin/ldconfig

    /bin/mkdir -m 700 -p %{_dbdir}

case "$1" in
    1)

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
        %{_sbindir}/configure-build.sh "%{_backupdir}"
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
        %{_lwisbindir}/lwregshell add_value "[HKEY_THIS_MACHINE\Software\VMware\Identity]" "Version" REG_SZ "%{_version}"
    else
        # set value if exists
        %{_lwisbindir}/lwregshell set_value "[HKEY_THIS_MACHINE\Software\VMware\Identity]" "Version" "%{_version}"
    fi
fi

%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

if [ "$1" = 0 ]; then
    /bin/systemctl >/dev/null 2>&1
    if [ $? -eq 0 ]; then

         if [ -f /etc/systemd/system/vmware-stsd.service ]; then
             /bin/systemctl stop vmware-stsd.service
             /bin/systemctl disable vmware-stsd.service
             /bin/rm -f /etc/systemd/system/vmware-stsd.service
             /bin/systemctl daemon-reload
         fi
    fi
fi

%postun

    /sbin/ldconfig

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

    case "$1" in
        0)
            /bin/rm -rf %{_dbdir}

            if [ -x "%{_lwisbindir}/lwregshell" ]
            then
                %{_lwisbindir}/lwregshell list_keys "[HKEY_THIS_MACHINE\Software\VMware\Identity]" > /dev/null 2>&1
                if [ $? -eq 0 ]; then
                    # delete key if exist
                    %{_lwisbindir}/lwregshell delete_tree "[HKEY_THIS_MACHINE\Software\VMware\Identity]"
                fi
            fi

            ;;
    esac

%files
%defattr(-,root,root,0755)
/lib/systemd/system/vmware-stsd.service
%{_sbindir}/vmware-stsd.sh
%{_sbindir}/configure-build.sh
%{_sbindir}/sso-config.sh
%{_includedir}/*.h
%{_lib64dir}/*.so*
%{_binsdir}/test-ldapbind
%{_binsdir}/test-logon
%{_binsdir}/test-svr
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
%{_webappsdir}/lightwaveui.war
%{_webappsdir}/ROOT.war
%{_datadir}/config/idm/*
%config %attr(600, root, root) %{_prefix}/vmware-sts/bin/setenv.sh
%config %attr(600, root, root) %{_prefix}/vmware-sts/bin/vmware-identity-tomcat-extensions.jar

%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/catalina.policy
%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/catalina.properties
%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/context.xml
%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/logging.properties
%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/server.xml
%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/web.xml
%config %attr(600, root, root) %{_prefix}/vmware-sts/conf/tomcat-users.xml

%files client
%defattr(-,root,root)
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
%{_jarsdir}/vmware-identity-depends.jar
%{_jarsdir}/openidconnect-client-lib.jar
%{_jarsdir}/vmware-identity-idm-client.jar
%{_jarsdir}/vmware-identity-idm-interface.jar
%{_jarsdir}/vmware-identity-rest-afd-client.jar
%{_jarsdir}/vmware-identity-rest-core-client.jar
%{_jarsdir}/vmware-identity-rest-idm-client.jar
%{_jarsdir}/vmware-directory-rest-client.jar
%{_includedir}/*.h
%{_lib64dir}/*.so*

%exclude %{_bindir}/*test

# %doc ChangeLog README COPYING

%files samples
%{_webappsdir}/openidconnect-sample-rp.war
%{_jarsdir}/vmware-identity-rest-idm-samples.jar

%changelog
*	Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.2.0-2
-	Renamed openjdk to openjdk8
*   Thu Mar 30 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-1
-   Initial - spec modified for Photon from lightwave git repo.
