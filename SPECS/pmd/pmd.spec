%define _mech_file /etc/gss/mech
%define _mech_id 1.3.6.1.4.1.6876.11711.2.1.2
%define _python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")
%define gssapi_unix_ver 1.0.0

Summary:        Photon Management Daemon
Name:           pmd
Version:        0.0.7
Release:        5%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache 2.0
URL:            https://www.github.com/vmware/%{name}
Group:          Applications/System

# PMD Source Code tarball
Source0:        %{name}-%{version}.tar.gz
%define sha1    pmd=97694042554dd10d99e5e4f15913a27dc22299b1

# gssapi_unix Source Code tarball
# GSSAPI-Unix URL: https://github.com/vmware/gssapi-unix
Source1:        gssapi-unix-%{gssapi_unix_ver}.tar.gz
%define sha1    gssapi-unix-%{gssapi_unix_ver}=5736db248f460f97203ac0c079dcc7862479e754

Requires:       copenapi
Requires:       c-rest-engine >= 1.1
Requires:       jansson
Requires:       network-config-manager
Requires:       systemd
Requires:       tdnf >= 2.1.1
Requires:       %{name}-libs = %{version}-%{release}
Requires:       shadow
Requires:       dcerpc
Requires:       openldap

BuildRequires:  copenapi-devel
BuildRequires:  c-rest-engine-devel >= 1.1
BuildRequires:  curl-devel
BuildRequires:  expat-devel
BuildRequires:  libsolv-devel
BuildRequires:  jansson-devel
BuildRequires:  krb5-devel
BuildRequires:  network-config-manager-devel
BuildRequires:  tdnf-devel >= 2.1.1
BuildRequires:  python3-devel >= 3.5
BuildRequires:  dcerpc-devel
BuildRequires:  openldap
BuildRequires:  openssl-devel
BuildRequires:  e2fsprogs-devel

%description
Photon Management Daemon

%package  libs
Summary:  photon management daemon libs
Requires: pmd-gssapi-unix = %{version}-%{release}

%description libs
photon management daemon libs used by server and clients

%package cli
Summary: photon management daemon cmd line cli
Requires: %{name}-libs = %{version}-%{release}

%description cli
photon management daemon cmd line cli

%package devel
Summary: photon management daemon client devel
Group: Development/Libraries

%description devel
photon management daemon client devel

%package python3
Summary: Python3 bindings for photon management daemon
Group: Development/Libraries
Requires: python3 >= 3.5
Requires: %{name}-cli = %{version}-%{release}

%description python3
Python3 bindings for photon management daemon

# sub-package: gssapi_unix
%package gssapi-unix
Summary:        gssapi-unix for unix authentication
Group:          System Environment/Security
Requires:       cyrus-sasl
Requires:       krb5
Requires:       dcerpc
Requires:       openldap
Requires:       openssl
Requires:       e2fsprogs

%description gssapi-unix
gssapi-unix for unix authentication

%prep
%autosetup -p1 -n %{name}-%{version}

# extract gssapi_unix code
cd ../
tar -xf %{SOURCE1} --no-same-owner

%build
sed -i 's,-lcrypto,-lcrypto -lgssapi_krb5 @top_builddir@/client/libpmdclient.la,' server/Makefile.am
autoreconf -mif
%configure \
    --disable-static \
    --enable-python=no
make %{?_smp_mflags}

pushd python
python3 setup.py build
popd

# Build gssapi_unix
cd ../gssapi-unix-%{gssapi_unix_ver}
export CFLAGS="-Wno-error=unused-but-set-variable -Wno-error=implicit-function-declaration -Wno-error=sizeof-pointer-memaccess -Wno-error=unused-local-typedefs -Wno-error=pointer-sign -Wno-error=address -Wno-unused-but-set-variable -Wno-unused-const-variable -Wno-misleading-indentation"
autoreconf -mif &&
aclocal && libtoolize && automake --add-missing && autoreconf &&
%configure \
    LDFLAGS=-ldl \
    --sysconfdir=/etc \
    --localstatedir=/var/lib/vmware
make %{?_smp_mflags}

%install
cd $RPM_BUILD_DIR/%{name}-%{version}
make DESTDIR=%{buildroot} install %{?_smp_mflags}
rm -f %{buildroot}%{_libdir}/*.la

pushd python
rm -f %{buildroot}%{python_sitearch}/pmd.so
python3 setup.py install --skip-build --root %{buildroot}
popd

install -d $RPM_BUILD_ROOT/var/log
install -d $RPM_BUILD_ROOT/var/opt/pmd/log
ln -sfv /var/opt/pmd/log $RPM_BUILD_ROOT/var/log/pmd
install -vdm755 %{buildroot}%{_unitdir}
install -D -m 444 pmd.service %{buildroot}%{_unitdir}
install -D -m 444 pmdprivsepd.service %{buildroot}%{_unitdir}
install -D -m 444 conf/restapispec.json %{buildroot}/etc/pmd/restapispec.json
install -D -m 444 conf/api_sddl.conf %{buildroot}/etc/pmd/api_sddl.conf
install -D -m 444 conf/restconfig.txt %{buildroot}/etc/pmd/restconfig.txt
install -d -m 0755 %{buildroot}/usr/lib/tmpfiles.d/
install -m 0644 conf/pmd-tmpfiles.conf %{buildroot}/usr/lib/tmpfiles.d/%{name}.conf
install -d -m 0755 %{buildroot}/etc/pmd.roles.d/
install -d -m 0755 %{buildroot}/etc/pmd.roles.plugins.d/

# gssapi_unix
cd ../gssapi-unix-%{gssapi_unix_ver}
make DESTDIR=%{buildroot} install %{?_smp_mflags}

# copy binaries for GSSAPI
mkdir -p %{buildroot}/%{_libdir}/gssapi_unix
mkdir -p %{buildroot}/%{_bindir}/gssapi_unix
mkdir -p %{buildroot}/%{_includedir}/gssapi_unix
mv %{buildroot}/%{_libdir}/libgssapi* %{buildroot}/%{_libdir}/gssapi_unix/
mv %{buildroot}/%{_bindir}/unix_srp %{buildroot}/%{_bindir}/gssapi_unix/
mv %{buildroot}/%{_includedir}/gssapi_creds_plugin.h %{buildroot}/%{_includedir}/gssapi_unix/
mv %{buildroot}/%{_includedir}/includes.h %{buildroot}/%{_includedir}/gssapi_unix/

# Pre-install
%pre
if ! getent group %{name} >/dev/null; then
    /sbin/groupadd -r %{name}
fi

if ! getent passwd %{name} >/dev/null; then
    /sbin/useradd -g %{name} %{name} -s /sbin/nologin
fi

# Post-install
%post
    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade
    sed -i "s/IPADDRESS_MARKER/`ifconfig eth0 | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'`/g" /etc/pmd/restapispec.json
    /sbin/ldconfig
    %systemd_post pmd.service
    %systemd_post pmdprivsepd.service

    if [ "$1" = 1 ]; then
      openssl req \
          -new \
          -newkey rsa:2048 \
          -days 365 \
          -nodes \
          -x509 \
          -subj "/C=US/ST=WA/L=Bellevue/O=vmware/CN=photon-pmd-default" \
          -keyout /etc/pmd/server.key \
          -out /etc/pmd/server.crt

      chmod 0400 /etc/pmd/server.key
      chown %{name} /etc/pmd/server.key
      openssl genrsa -out /etc/pmd/privsep_priv.key 2048
      openssl rsa -in /etc/pmd/privsep_priv.key -pubout > /etc/pmd/privsep_pub.key
      chmod 0400 /etc/pmd/privsep*.key
      chown %{name} /etc/pmd/privsep_pub.key
    fi
    %tmpfiles_create %_tmpfilesdir/%{name}.conf

# Pre-uninstall
%preun
    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade
    %systemd_preun pmd.service
    %systemd_preun pmdprivsepd.service

# Post-uninstall
%postun
    /sbin/ldconfig

    %systemd_postun_with_restart pmd.service
    %systemd_postun_with_restart pmdprivsepd.service

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade
if [ $1 -eq 0 ] ; then
    if getent passwd %{name} >/dev/null; then
        /sbin/userdel %{name}
    fi
    if getent group %{name} >/dev/null; then
        /sbin/groupdel %{name}
    fi
fi

# Post-uninstall
%postun cli
    /sbin/ldconfig

%post gssapi-unix
    # Create directory "/usr/lib/gss" if not exist
    if [ ! -d "%{_libdir}/gss" ] ; then
        mkdir -p %{_libdir}/gss
    fi

    # Create directory "/etc/gss" if not exist
    if [ ! -d "%{_sysconfdir}/gss" ] ; then
        mkdir -p %{_sysconfdir}/gss
    fi

    # Create file "/etc/gss/mech" if not exist
    if [ ! -f "%{_mech_file}" ]; then
        touch %{_mech_file}
    fi

    # Add symlink of libgssapi_unix_creds.so to %{_libdir} directory
    if [ ! -h %{_libdir}/libgssapi_unix_creds.so ]; then
        /bin/ln -s %{_libdir}/gssapi_unix/libgssapi_unix_creds.so %{_libdir}/libgssapi_unix_creds.so
    fi

    # Add libgssapi_unix.so to gssapi_unix directory
    if [ ! -h %{_libdir}/gss/libgssapi_unix.so ]; then
        /bin/ln -sf %{_libdir}/gssapi_unix/libgssapi_unix.so %{_libdir}/gss/libgssapi_unix.so
    fi

    # Update file "/etc/gss/mech" with GSSAPI mech_id
    if [ -f "%{_mech_file}" ]; then
        if [ `grep -c "%{_mech_id}" "%{_mech_file}"` -lt 1 ]; then
            echo "unix %{_mech_id} libgssapi_unix.so" >> "%{_mech_file}"
        fi
    fi

    chmod 644 %{_mech_file}

    /sbin/ldconfig

# Pre-uninstall gssapi-unix
%preun gssapi-unix

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

if [ "$1" = 0 ]; then
    # Cleanup libgssapi_unix_creds.so symlink
    if [ -h %{_libdir}/libgssapi_unix_creds.so ]; then
        rm -f %{_libdir}/libgssapi_unix_creds.so
    fi

    # Cleanup GSSAPI UNIX symlink
    if [ -h %{_libdir}/gss/libgssapi_unix.so ]; then
        rm -f %{_libdir}/gss/libgssapi_unix.so
    fi

    # Remove GSSAPI configuration from GSS mech file
    if [ -f "%{_mech_file}" ]; then
        if [ `grep -c  "%{_mech_id}" "%{_mech_file}"` -gt 0 ]; then
            cat "%{_mech_file}" | sed '/%{_mech_id}/d' > "/tmp/mech-$$"
            if [ -s /tmp/mech-$$ ]; then
                mv "/tmp/mech-$$" "%{_mech_file}"
            fi
        fi
    fi
fi

%check
pushd tests/net
# pmd-cli net tests
python3 pmd_net_cli.py
# pmd.server.net python3 tests
python3 pmd_net_python3.py
popd

%clean
rm -rf %{buildroot}/*

%files
    %defattr(-,root,root,0755)
    %{_bindir}/pmd
    %{_bindir}/pmdprivsepd
    %{_libdir}/systemd/system/pmd.service
    %{_libdir}/systemd/system/pmdprivsepd.service
    /etc/pmd/pmd.conf
    /etc/pmd/api_sddl.conf
    /etc/pmd/restapispec.json
    /etc/pmd/restconfig.txt
    %attr(0766, %{name}, %{name}) %dir /var/opt/%{name}/log
    %attr(0766, %{name}, %{name}) /var/log/%{name}
    %_tmpfilesdir/%{name}.conf
    %dir /etc/pmd.roles.plugins.d/
    %dir /etc/pmd.roles.d/

%files libs
    %defattr(-,root,root)
    %{_libdir}/libpmdclient.so*

%files cli
    %defattr(-,root,root)
    %{_bindir}/pmd-cli
    %exclude %{_libdir}/libpmdclient.a

%files devel
    %defattr(-,root,root)
    %{_includedir}/pmd/*.h
    %{_libdir}/pkgconfig/pmdclient.pc

%files python3
    %defattr(-,root,root)
    %{_python3_sitearch}/%{name}/
    %{_python3_sitearch}/%{name}_python-*.egg-info

# gssapi_unix
%files gssapi-unix
    %defattr(-,root,root)
    %dir %{_libdir}/gssapi_unix
    %dir %{_bindir}/gssapi_unix
    %dir %{_includedir}/gssapi_unix
    %{_libdir}/gssapi_unix/*.so*
    %{_bindir}/gssapi_unix/unix_srp
    %{_includedir}/gssapi_unix/*.h
    %exclude %{_libdir}/gssapi_unix/*.a
    %exclude %{_libdir}/gssapi_unix/*.la

%changelog
*   Tue Jun 01 2021 <okurth@vmware.com> 0.0.7-5
-   Bump to consume latest tdnf
*   Mon Apr 12 2021 Shreyas B <shreyasb@vmware.com> 0.0.7-4
-   Use GSSAPI-Unix Code from github
-   Support for openssl v1.1.1 added to GSSAPI-Unix Code
*   Sat Feb 20 2021 Tapas Kundu <tkundu@vmware.com> 0.0.7-3
-   Update to 0.0.7-GA
*   Fri Feb 19 2021 Tapas Kundu <tkundu@vmware.com> 0.0.7-2
-   Bump to consume latest tdnf
*   Thu Dec 24 2020 Tapas Kundu <tkundu@vmware.com> 0.0.7-1
-   Update to 0.0.7-beta
-   Added support for network-config-manager
-   Support for "pmd-cli net" and python3 "server.net"
-   Added test directory which includes tests for both
-   pmd-cli and python3 for net to test changes locally
-   Removed support for netmgmt
*   Thu Nov 19 2020 Shreyas B <shreyasb@vmware.com> 0.0.6-7
-   Remove LightWave & LikeWise dependency.
-   Add dcerpc & openldap dependency.
-   Build gssapi_unix as subpackage of PMD.
-   Support for OpenSSL v1.1.1.
-   Fix Build issues.
*   Tue Nov 03 2020 Tapas Kundu <tkundu@vmware.com> 0.0.6-6
-   Added null check for pszgpgkeys
*   Tue Oct 27 2020 Keerthana K <keerthanak@vmware.com> 0.0.6-5
-   Build with tdnf v3.0.0-beta
*   Sat Jun 20 2020 Tapas Kundu <tkundu@vmware.com> 0.0.6-4
-   Mass removal python2
*   Thu Jun 04 2020 Tapas Kundu <tkundu@vmware.com> 0.0.6-3
-   Build with tdnf 2.1.1
*   Tue Feb 25 2020 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.6-2
-   apply patch for tdnf-2.1.0
*   Mon Sep 30 2019 Tapas Kundu <tkundu@vmware.com> 0.0.6-1
-   Updated to release 0.0.6
-   Included role mgmt changes.
*   Wed Jan 23 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.5-9
-   Fix a bug in firewall management persist commands
*   Tue Dec 18 2018 Tapas Kundu <tkundu@vmware.com> 0.0.5-8
-   Fix for if_iaid and duid.
*   Tue Dec 11 2018 Michelle Wang <michellew@vmware.com> 0.0.5-7
-   DNS_MODE_INVALID is renamed with DNS_MODE_UNKNOWN in netmgmt 1.2.0.
*   Thu Mar 01 2018 Xiaolin Li <xiaolinl@vmware.com> 0.0.5-6
-   Build with tdnf 2.0.0.
*   Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  0.0.5-5
-   Fixed the log file directory structure
*   Thu Nov 30 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.5-4
-   update to use c-rest-engine-1.11
*   Tue Oct 24 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.5-3
-   Bug fixes and net commands fixes
*   Sat Sep 30 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.5-2
-   Apply patch for local rpc connection separation
-   patch for couple of minor coverity scan fixes.
*   Thu Sep 28 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.5-1
-   Update to version 0.0.5
*   Sat Sep 23 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.4-1
-   Add privilege separation
*   Tue Aug 01 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.3-1
-   Fix REST param handling, CLI locale.
*   Thu Jun 01 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.2-1
-   Fix python3 string issues.
*   Tue May 23 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.1-2
-   Changes for lightwave dependencies
*   Thu May 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.0.1-1
-   Initial build.  First version
