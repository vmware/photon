#
# pmd spec file
#

%define _mech_file /etc/gss/mech
%define _mech_id 1.3.6.1.4.1.6876.11711.2.1.2
%define _python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")

Summary:	Photon Management Daemon
Name:		pmd
Version:	0.0.3
Release:	1%{?dist}
Vendor:		VMware, Inc.
Distribution:	Photon
License:	Apache 2.0
URL:            https://www.github.com/vmware/pmd
Group:		Applications/System
Requires:       copenapi
Requires:	c-rest-engine
Requires:       jansson
Requires:	likewise-open >= 6.2.9
Requires:       netmgmt
Requires:	systemd
Requires:	tdnf >= 1.2.0
Requires:       lightwave-client-libs
BuildRequires:  copenapi-devel
BuildRequires:	c-rest-engine-devel
BuildRequires:	curl-devel
BuildRequires:	hawkey-devel >= 2017.1
BuildRequires:  jansson-devel
BuildRequires:	krb5-devel
BuildRequires:	likewise-open-devel >= 6.2.9
BuildRequires:	netmgmt-cli-devel
BuildRequires:	netmgmt-devel
BuildRequires:	tdnf-devel >= 1.2.0
BuildRequires:  lightwave-devel
Source0:	%{name}-%{version}.tar.gz
%define sha1 pmd=db86a13cc82c4daff2f329d25a9e8d22c2184c3a
Source1:        pmd.service

%description
Photon Management Daemon

%package cli
Summary: photon management daemon cmd line cli
Requires: likewise-open >= 6.2.0
Requires: lightwave-client-libs

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
sed -i 's/pmd, 0.0.1/pmd, 0.0.3/' configure.ac
sed -i 's,-lcrypto,-lcrypto @LWBASE_LIBS@ -lgssapi_krb5,' server/Makefile.am
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
make

pushd python
python2 setup.py build
python3 setup.py build
popd

%install
cd $RPM_BUILD_DIR/%{name}-%{version}
make DESTDIR=%{buildroot} install

pushd python
python2 setup.py install --skip-build --root %{buildroot}
rm -f %{buildroot}%{python_sitearch}/pmd.so
python3 setup.py install --skip-build --root %{buildroot}
popd

install -d $RPM_BUILD_ROOT/var/log/pmd
install -vdm755 %{buildroot}%{_unitdir}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -D -m 444 conf/restapispec.json %{buildroot}/etc/pmd/restapispec.json
install -D -m 444 conf/api_sddl.conf %{buildroot}/etc/pmd/api_sddl.conf
install -D -m 444 conf/restconfig.txt %{buildroot}/etc/pmd/restconfig.txt
install -D -m 444 conf/server.crt  %{buildroot}/etc/pmd/server.crt
install -D -m 444 conf/server.key %{buildroot}/etc/pmd/server.key

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

    if [ ! -d "%{_libdir}/gss" ] ; then
        mkdir %{_libdir}/gss
    fi

    # Add libgssapi_unix.so to GSSAPI plugin directory
    if [ ! -h %{_libdir}/gss/libgssapi_unix.so ]; then
        /bin/ln -sf %{_libdir}/libgssapi_unix.so %{_libdir}/gss/libgssapi_unix.so
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
        /bin/ln -sf %{_libdir}/libgssapi_unix.so %{_libdir}/gss/libgssapi_unix.so
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
    %{_libdir}/*.la
    %{_libdir}/libpmdclient.so
    %{_libdir}/pkgconfig/pmdclient.pc

%files python2
    %{python_sitearch}/%{name}/
    %{python_sitearch}/%{name}_python-*.egg-info

%files python3
    %{_python3_sitearch}/%{name}/
    %{_python3_sitearch}/%{name}_python-*.egg-info

%changelog
*       Tue Aug 01 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.3-1
-       Fix REST param handling, CLI locale.
*       Thu Jun 01 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.2-1
-       Fix python3 string issues.
*       Tue May 23 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.1-2
-       Changes for lightwave dependencies
*       Thu May 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.1-1
-       Initial build.  First version
