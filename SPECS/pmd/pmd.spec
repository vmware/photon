#
# pmd spec file
#

%define _mech_file /etc/gss/mech
%define _mech_id 1.3.6.1.4.1.6876.11711.2.1.2
%define _python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")

Summary:        Photon Management Daemon
Name:           pmd
Version:        0.0.5
Release:        7%{?dist}
Vendor:         VMware, Inc.
Distribution:   Photon
License:        Apache 2.0
URL:            https://www.github.com/vmware/pmd
Group:          Applications/System
Requires:       copenapi
Requires:       c-rest-engine >= 1.1
Requires:       jansson
Requires:       likewise-open >= 6.2.9
Requires:       netmgmt
Requires:       systemd
Requires:       tdnf >= 2.0.0
Requires:       lightwave-client-libs
Requires:       %{name}-libs = %{version}-%{release}
Requires:       shadow
BuildRequires:  copenapi-devel
BuildRequires:  c-rest-engine-devel >= 1.1
BuildRequires:  curl-devel
BuildRequires:  libsolv-devel
BuildRequires:  jansson-devel
BuildRequires:  krb5-devel
BuildRequires:  likewise-open-devel >= 6.2.9
BuildRequires:  netmgmt-cli-devel
BuildRequires:  netmgmt-devel
BuildRequires:  tdnf-devel >= 1.2.0
BuildRequires:  lightwave-devel
Source0:        %{name}-%{version}-3.tar.gz
%define sha1    pmd=fe9b4b81410497d209fc4b6efb9574a049557b25
Patch0:         pmd-update-to-c-rest-engine-1.1.patch
Patch1:         pmd-rename-DNS_MODE_INVALID-with-DNS_MODE_UNKNOWN.patch

%description
Photon Management Daemon

%package libs
Summary: photon management daemon libs
Requires: likewise-open >= 6.2.0

%description libs
photon management daemon libs used by server and clients

%package cli
Summary: photon management daemon cmd line cli
Requires: %{name}-libs = %{version}-%{release}
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
%patch0 -p1
%patch1 -p1

%build
sed -i 's/pmd, 0.0.1/pmd, 0.0.5/' configure.ac
sed -i 's,-lcrypto,-lcrypto -lgssapi_krb5 @top_builddir@/client/libpmdclient.la,' server/Makefile.am
autoreconf -mif
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --sysconfdir=/etc \
    --with-likewise=/opt/likewise \
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
rm -f %{buildroot}%{_libdir}/*.la

pushd python
python2 setup.py install --skip-build --root %{buildroot}
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
    %{_bindir}/pmdprivsepd
    /lib/systemd/system/pmd.service
    /lib/systemd/system/pmdprivsepd.service
    /etc/pmd/pmd.conf
    /etc/pmd/api_sddl.conf
    /etc/pmd/restapispec.json
    /etc/pmd/restconfig.txt
    %attr(0766, %{name}, %{name}) %dir /var/opt/%{name}/log
    %attr(0766, %{name}, %{name}) /var/log/%{name}
    %_tmpfilesdir/%{name}.conf

%files libs
    %{_libdir}/libpmdclient.so*

%files cli
    %{_bindir}/pmd-cli

%files devel
    %{_includedir}/pmd/*.h
    %{_libdir}/pkgconfig/pmdclient.pc

%files python2
    %{python_sitearch}/%{name}/
    %{python_sitearch}/%{name}_python-*.egg-info

%files python3
    %{_python3_sitearch}/%{name}/
    %{_python3_sitearch}/%{name}_python-*.egg-info

%changelog
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
