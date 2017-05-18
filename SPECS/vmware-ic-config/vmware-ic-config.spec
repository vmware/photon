Name:          vmware-ic-config
Summary:       VMware Infrastructure Controller Configuration Tool
Version:       1.2.0
Release:       2%{?dist}
License:       Apache 2.0
Group:         Applications/System
Vendor:        VMware, Inc.
URL: 	       https://github.com/vmware/lightwave
Source0:       lightwave-%{version}.tar.gz
%define sha1 lightwave=5f8bb80732e5f03df321c52bf12c305e65ad66a3
Patch0:        ic_config_build_fixes.patch
Distribution:  Photon

Requires:  coreutils >= 8.22
Requires:  openssl >= 1.0.2
Requires:  likewise-open >= 6.2.11
Requires:  vmware-directory-client = %{version}
Requires:  vmware-afd-client = %{version}
Requires:  vmware-ca-client = %{version}
Requires:  gawk >= 4.1.3

BuildRequires:  coreutils >= 8.22
BuildRequires:  curl-devel
BuildRequires:  jansson-devel
BuildRequires:  likewise-open-devel >= 6.2.11
BuildRequires:  openssl-devel >= 1.0.2
BuildRequires:  vmware-directory = %{version}
BuildRequires:  vmware-directory-client-devel = %{version}
BuildRequires:  vmware-afd-client-devel = %{version}
BuildRequires:  vmware-ca-client-devel = %{version}
BuildRequires:  vmware-dns-client-devel = %{version}
BuildRequires:  vmware-sts = %{version}
BuildRequires:  openjdk8 >= 1.8.0.112-2, apache-ant >= 1.9.6-6
BuildRequires:  ant-contrib >= 1.0b3
BuildRequires:  apache-maven >= 3.3.9-8

%define _prefix /opt/vmware
%define _includedir %{_prefix}/include
%define _lib64dir %{_prefix}/lib64
%define _bindir %{_prefix}/bin
%define _sbindir %{_prefix}/sbin
%define _datadir %{_prefix}/share

%define _bindir %{_prefix}/bin
%define _configdir %{_prefix}/share/config
%define _serviceddir /lib/systemd/system
%define _jarsdir  %{_prefix}/jars

%if 0%{?_likewise_open_prefix:1} == 0
%define _likewise_open_prefix /opt/likewise
%endif

%define _jreextdir %{_java_home}/jre/lib/ext

%if 0%{?_vmdir_prefix:1} == 0
%define _vmdir_prefix /opt/vmware
%endif

%if 0%{?_vmafd_prefix:1} == 0
%define _vmafd_prefix /opt/vmware
%endif

%if 0%{?_vmca_prefix:1} == 0
%define _vmca_prefix /opt/vmware
%endif

%if 0%{?_vmdns_prefix:1} == 0
%define _vmdns_prefix /opt/vmware
%endif

%if 0%{?_vmsts_prefix:1} == 0
%define _vmsts_prefix /opt/vmware
%endif

%description
VMware Infrastructure Controller Configuration Tool

%prep
%setup -qn lightwave-%{version}
%patch0 -p1

%build

cd config/build
autoreconf -mif .. &&
../configure --prefix=%{_prefix} \
             --libdir=%{_lib64dir} \
             --with-likewise=%{_likewise_open_prefix} \
             --with-vmdir=%{_vmdir_prefix} \
             --with-vmca=%{_vmca_prefix} \
             --with-vmdns=%{_vmdns_prefix} \
             --with-afd=%{_vmafd_prefix} \
             --with-sts=%{_vmsts_prefix} \
             --with-ssl=/usr \
             --with-java=%{_java_home} \
             --with-ant=%{_ant_home} \
             --with-maven=%{_maven_home} \
             --disable-static
make

%install

[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
cd config/build && make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete

%pre

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

%post

    # First argument is 1 => New Installation
    # First argument is 2 => Upgrade

    /sbin/ldconfig

    /bin/systemctl enable firewall.service >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        /bin/ln -s %{_serviceddir}/firewall.service /etc/systemd/system/multi-user.target.wants/firewall.service 
    fi

    /bin/systemctl >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        /bin/systemctl daemon-reload
    fi
    /bin/systemctl start firewall.service

%preun

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade
    /bin/systemctl >/dev/null 2>&1
    if [ $? -eq 0 ]; then

         if [ -f /etc/systemd/system/firewall.service ]; then
             /bin/systemctl stop firewall.service
             /bin/systemctl disable firewall.service
             /bin/rm -f /etc/systemd/system/firewall.service
             /bin/systemctl daemon-reload
         fi

    fi

%postun

    /sbin/ldconfig

    # First argument is 0 => Uninstall
    # First argument is 1 => Upgrade

%files
%defattr(-,root,root,0755)
%{_bindir}/ic-promote
%{_bindir}/ic-join
%{_bindir}/configure-lightwave-server
%{_bindir}/configure-identity-server
%{_bindir}/domainjoin.sh
%{_lib64dir}/*.so*
%{_jarsdir}/*.jar
%{_configdir}/firewall.json
%{_configdir}/setfirewallrules.py
%{_serviceddir}/firewall.service

# %doc ChangeLog README COPYING

%changelog
*	Thu May 18 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.2.0-2
-	Renamed openjdk to openjdk8
*   Thu Mar 30 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.0-1
-   Initial - spec modified for Photon from lightwave git repo.
