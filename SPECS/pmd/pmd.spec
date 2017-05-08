%define _mech_file /etc/gss/mech
%define _mech_id 1.3.6.1.4.1.6876.11711.2.1.2
%define _python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")

Summary:	Photon Management Daemon
Name:		pmd
Version:	0.1
Release:	1%{?dist}
Vendor:		VMware, Inc.
Distribution:	Photon
License:	Apache 2.0
URL:            https://www.github.com/vmware/copenapi
Group:		Applications/System
Requires:	likewise-open >= 6.2.9
Requires:       netmgmt
Requires:	systemd
Requires:	tdnf >= 1.2.0
Requires:	vmware-rest
Requires:       vmware-afd-client
Requires:       vmware-directory-client
Requires:       jansson
Requires:       copenapi
BuildRequires:	popt-devel
BuildRequires:	rpm-devel
BuildRequires:	tdnf-devel >= 1.2.0
BuildRequires:	vmware-rest-devel
BuildRequires:  vmware-afd-client-devel
BuildRequires:  vmware-directory-client-devel
BuildRequires:	netmgmt-devel
BuildRequires:  jansson-devel
BuildRequires:  copenapi-devel
BuildRequires:	likewise-open-devel >= 6.2.9
BuildRequires:	krb5-devel
BuildRequires:	glib-devel
BuildRequires:	curl-devel
Source0:	%{name}-%{version}.tar.gz
%define sha1 pmd=ddf92e1b69c95d18e59a38f76b848b633bc68d6f

%description
Photon Management Daemon

%package cli
BuildRequires:	netmgmt-cli-devel >= 1.0.4-2
Summary: photon management daemon cmd line cli
Requires: likewise-open >= 6.2.0
Requires: vmware-directory-client

%description cli
photon management daemon cmd line cli

%package devel
Summary: photon management daemon client devel
Group: Development/Libraries

%description devel
photon management daemon client devel

%package python2
Summary: Python2 bindings for photon management daemon
Group: Development/Libraries
Requires: python2 >= 2.7
Requires: %{name}-cli = %{version}-%{release}
BuildRequires: python2-devel >= 2.7

%description python2
Python2 bindings for photon management daemon

%package python3
Summary: Python3 bindings for photon management daemon
Group: Development/Libraries
Requires: python3 >= 3.5
Requires: %{name}-cli = %{version}-%{release}
BuildRequires: python3-devel >= 3.5

%description python3
Python3 bindings for photon management daemon

%prep
%setup -q

%build
cd $RPM_BUILD_DIR/%{name}-%{version}
autoreconf -mif
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --sysconfdir=/etc \
    --with-likewise=/opt/likewise \
    --with-vmware-rest=/usr/lib \
    --enable-python=no \
    --disable-static
make clean
make

pushd python
python2 setup.py build
python3 setup.py build
popd

%install
cd $RPM_BUILD_DIR/%{name}-%{version}
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_libdir}/*.la

pushd python
python2 setup.py install --skip-build --root %{buildroot}
rm -f %{buildroot}%{python_sitearch}/pmd.so
python3 setup.py install --skip-build --root %{buildroot}
popd

install -d $RPM_BUILD_ROOT/var/log/pmd
install -D -m 444 pmd.service %{buildroot}/lib/systemd/system/pmd.service
install -D -m 444 restconf/restapispec.json %{buildroot}/etc/pmd/restapispec.json
install -D -m 444 api_sddl.conf %{buildroot}/etc/pmd/api_sddl.conf
install -D -m 444 restconf/restconfig.txt %{buildroot}/etc/pmd/restconfig.txt
install -D -m 444 restconf/server.crt  %{buildroot}/etc/pmd/server.crt
install -D -m 444 restconf/server.key %{buildroot}/etc/pmd/server.key

# Pre-install
%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

# Post-install
%post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade
    sed -i "s/IPADDRESS_MARKER/`ifconfig eth0 | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'`/g" /etc/pmd/restapispec.json
    /sbin/ldconfig
    %systemd_post pmd.service
    systemctl daemon-reload
    systemctl restart pmd
    #open port 81 for REST server
    iptables -A INPUT -p tcp --dport 81 -j ACCEPT
    #open port 2016 for dcerpc server
    iptables -A INPUT -p tcp --dport 2016 -j ACCEPT
    #persist firewall info

    if [ ! -d "%{_libdir}/gss" ] ; then
        mkdir %{_libdir}/gss
    fi

    # Add libgssapi_unix.so to GSSAPI plugin directory
    if [ ! -h %{_libdir}/gss/libgssapi_unix.so ]; then
        /bin/ln -sf /opt/vmware/lib64/libgssapi_unix.so %{_libdir}/gss/libgssapi_unix.so
    fi
    # Add gssapi_unix plugin configuration to GSS mech file
    if [ -f "%{_mech_file}" ]; then
        if [ `grep -c "%{_mech_id}" "%{_mech_file}"` -lt 1 ]; then
            echo "unix %{_mech_id} libgssapi_unix.so" >> "%{_mech_file}"
        fi
    fi

# Pre-uninstall
%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade
    %systemd_preun pmd.service
if [ "$1" = 0 ]; then
    if [ ! -e %{_bindir}/pmd-cli ]; then
        # Cleanup GSSAPI UNIX symlink
        if [ -h %{_libdir}/gss/libgssapi_unix.so ]; then
            rm -f %{_libdir}/gss/libgssapi_unix.so
        fi
        # Remove GSSAPI SRP plugin configuration from GSS mech file
        if [ -f "%{_mech_file}" ]; then
            if [ `grep -c  "%{_mech_id}" "%{_mech_file}"` -gt 0 ]; then
                cat "%{_mech_file}" | sed '/%{_mech_id}/d' > "/tmp/mech-$$"
                if [ -s /tmp/mech-$$ ]; then
                    mv "/tmp/mech-$$" "%{_mech_file}"
                fi
            fi
        fi
    fi
fi


# Post-uninstall
%postun

    /sbin/ldconfig

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade
    %systemd_postun_with_restart pmd.service

# Post pmd-cli
%post cli
    if [ ! -d "%{_libdir}/gss" ] ; then
        mkdir %{_libdir}/gss
    fi

    # Add libgssapi_unix.so to GSSAPI plugin directory
    if [ ! -h %{_libdir}/gss/libgssapi_unix.so ]; then
        /bin/ln -sf /opt/vmware/lib64/libgssapi_unix.so %{_libdir}/gss/libgssapi_unix.so
    fi
    # Add gssapi_unix plugin configuration to GSS mech file
    if [ -f "%{_mech_file}" ]; then
        if [ `grep -c "%{_mech_id}" "%{_mech_file}"` -lt 1 ]; then
            echo "unix %{_mech_id} libgssapi_unix.so" >> "%{_mech_file}"
        fi
    fi

# Pre-uninstall cli
%preun cli

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

if [ "$1" = 0 ]; then
    if [ ! -e %{_bindir}/pmd ]; then
        # Cleanup GSSAPI UNIX symlink
        if [ -h %{_libdir}/gss/libgssapi_unix.so ]; then
            rm -f %{_libdir}/gss/libgssapi_unix.so
        fi
        # Remove GSSAPI SRP plugin configuration from GSS mech file
        if [ -f "%{_mech_file}" ]; then
            if [ `grep -c  "%{_mech_id}" "%{_mech_file}"` -gt 0 ]; then
                cat "%{_mech_file}" | sed '/%{_mech_id}/d' > "/tmp/mech-$$"
                if [ -s /tmp/mech-$$ ]; then
                    mv "/tmp/mech-$$" "%{_mech_file}"
                fi
            fi
        fi
    fi
fi
# Post-uninstall
%postun cli
    /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
    %defattr(-,root,root,0755)
    %{_bindir}/pmd
    /lib/systemd/system/pmd.service
    /etc/pmd/pmd.conf
    /etc/pmd/api_sddl.conf
    /etc/pmd/restapispec.json
    /etc/pmd/restconfig.txt
    /etc/pmd/server.crt
    /etc/pmd/server.key
    %dir /var/log/pmd

%files cli
    %{_bindir}/pmd-cli
    %{_libdir}/libpmdclient.so.*

%files devel
    %{_includedir}/pmd/*.h
    %{_libdir}/libpmdclient.so
    %{_libdir}/pkgconfig/pmdclient.pc

%files python2
    %{python_sitearch}/%{name}/
    %{python_sitearch}/%{name}_python-*.egg-info

%files python3
    %{_python3_sitearch}/%{name}/
    %{_python3_sitearch}/%{name}_python-*.egg-info

%changelog
*       Thu May 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.1-1
-       Initial build.  First version
