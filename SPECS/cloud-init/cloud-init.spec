%define python3_sitelib /usr/lib/python3.6/site-packages

Name:           cloud-init
Version:        0.7.9
Release:        9%{?dist}
Summary:        Cloud instance init scripts
Group:          System Environment/Base
License:        GPLv3
URL:            http://launchpad.net/cloud-init
Source0:        https://launchpad.net/cloud-init/trunk/%{version}/+download/%{name}-%{version}.tar.gz
%define sha1 cloud-init=3b4345267e72e28b877e2e3f0735c1f672674cfc
Source1:        cloud-photon.cfg
Source2:        99-disable-networking-config.cfg

Patch0:         photon-distro.patch
Patch1:         change-requires.patch
Patch2:         vca-admin-pwd.patch
Patch3:         photon-hosts-template.patch
Patch4:         resizePartitionUUID.patch
Patch5:         datasource-guestinfo.patch
Patch6:         systemd-service-changes.patch

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  systemd
BuildRequires:  dbus
BuildRequires:  python3-ipaddr
BuildRequires:  iproute2
BuildRequires:  automake
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       systemd
Requires:       net-tools
Requires:       python3
Requires:       python3-libs
Requires:       python3-configobj
Requires:       python3-prettytable
Requires:       python3-requests
Requires:       python3-PyYAML
Requires:       python3-jsonpatch
Requires:       python3-oauthlib
Requires:       python3-jinja2
Requires:       python3-markupsafe
Requires:       python3-six
Requires:       python3-setuptools
Requires:       python3-xml
BuildArch:      noarch

%description
Cloud-init is a set of init scripts for cloud instances.  Cloud instances
need special scripts to run during initialization to retrieve and install
ssh keys and to let the user run various scripts.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

find systemd -name cloud*.service | xargs sed -i s/StandardOutput=journal+console/StandardOutput=journal/g

%build
python3 setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python3 setup.py install -O1 --skip-build --root=%{buildroot} --init-system systemd

# Don't ship the tests
rm -r %{buildroot}%{python3_sitelib}/tests

mkdir -p %{buildroot}/var/lib/cloud
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/cloud/cloud.cfg.d/

# We supply our own config file since our software differs from Ubuntu's.
cp -p %{SOURCE1} %{buildroot}/%{_sysconfdir}/cloud/cloud.cfg

# Disable networking config by cloud-init
cp -p %{SOURCE2} $RPM_BUILD_ROOT/%{_sysconfdir}/cloud/cloud.cfg.d/

%check
openssl req \
    -new \
    -newkey rsa:4096 \
    -days 365 \
    -nodes \
    -x509 \
    -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=photon.com" \
    -keyout photon.key \
    -out photon.cert
     openssl rsa -in photon.key -out photon.pem
mv photon.pem /etc/ssl/certs   

easy_install pip
easy_install -U setuptools
easy_install HTTPretty 
easy_install mocker
easy_install mock
easy_install nose
easy_install pep8
easy_install pyflakes
easy_install pyyaml
easy_install pyserial
easy_install oauth2
easy_install oauth
easy_install cheetah
easy_install jinja2
easy_install PrettyTable
easy_install argparse
easy_install requests
easy_install jsonpatch
easy_install configobj

sed -i '38,43d' tests/unittests/test_handler/test_handler_set_hostname.py
mkdir -p /etc/sysconfig
echo "HOSTNAME=test.com" >/etc/sysconfig/network
make test

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post cloud-config.service
%systemd_post cloud-final.service
%systemd_post cloud-init.service
%systemd_post cloud-init-local.service

%preun
%systemd_preun cloud-config.service
%systemd_preun cloud-final.service
%systemd_preun cloud-init.service
%systemd_preun cloud-init-local.service

%postun
%systemd_postun cloud-config.service
%systemd_postun cloud-final.service
%systemd_postun cloud-init.service
%systemd_postun cloud-init-local.service

%files
%license LICENSE
%doc %{_sysconfdir}/cloud/cloud.cfg.d/README
%dir %{_sysconfdir}/cloud/templates
%config(noreplace) %{_sysconfdir}/cloud/templates/*
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg.d/05_logging.cfg
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg
%config(noreplace) %{_sysconfdir}/cloud/cloud.cfg.d/99-disable-networking-config.cfg
%{_sysconfdir}/NetworkManager/dispatcher.d/hook-network-manager
%{_sysconfdir}/dhcp/dhclient-exit-hooks.d/hook-dhclient
/lib/systemd/system-generators/cloud-init-generator
/lib/udev/rules.d/66-azure-ephemeral.rules
/lib/systemd/system/*
%{_docdir}/cloud-init/*
%{_libdir}/cloud-init/*
%{python3_sitelib}/*
%{_bindir}/cloud-init*
%dir /var/lib/cloud


%changelog
*   Wed Jul 19 2017 Divya Thaluru <dthaluru@vmware.com> 0.7.9-9
-   Enabled openstack provider
*   Wed Jun 28 2017 Anish Swaminathan <anishs@vmware.com> 0.7.9-8
-   Restart network service in bring_up_interfaces
*   Thu Jun 22 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.9-7
-   Add python3-setuptools and python3-xml to requires.
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.9-6
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Mon Jun 5 2017 Julian Vassev <jvassev@vmware.com> 0.7.9-5
-   Enable OVF datasource by default
*   Mon May 22 2017 Kumar Kaushik <kaushikk@vmware.com> 0.7.9-4
-   Making cloud-init to use python3.
*   Thu May 15 2017 Anish Swaminathan <anishs@vmware.com> 0.7.9-3
-   Disable networking config by cloud-init
*   Thu May 04 2017 Anish Swaminathan <anishs@vmware.com> 0.7.9-2
-   Support userdata in vmx guestinfo
*   Thu Apr 27 2017 Anish Swaminathan <anishs@vmware.com> 0.7.9-1
-   Upgraded to version 0.7.9
-   Enabled VmxGuestinfo datasource
*   Thu Apr 27 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.6-17
-   Fix Arch
*   Wed Mar 29 2017 Kumar Kaushik <kaushikk@vmware.com>  0.7.6-16
-   Adding support for disk partition and resize fs
*   Thu Dec 15 2016 Dheeraj Shetty <dheerajs@vmware.com>  0.7.6-15
-   Adding template file and python-jinja2 dependency to update hosts
*   Tue Dec 13 2016 Dheeraj Shetty <dheerajs@vmware.com>  0.7.6-14
-   Fixed restarting of sshd daemon
*   Tue Nov 22 2016 Kumar Kaushik <kaushikk@vmware.com>  0.7.6-13
-   Adding flag for vmware customization in config.
*   Tue Nov 1 2016 Divya Thaluru <dthaluru@vmware.com>  0.7.6-12
-   Fixed logic to not restart services after upgrade
*   Mon Oct 24 2016 Divya Thaluru <dthaluru@vmware.com>  0.7.6-11
-   Enabled ssh module in cloud-init
*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  0.7.6-10
-   Fixed logic to restart the active services after upgrade 
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.6-9
-   GA - Bump release of all rpms
*   Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  0.7.6-8
-   Clean up post, preun, postun sections in spec file.
*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>
-   Add systemd to Requires and BuildRequires.
*   Thu Sep 17 2015 Kumar Kaushik <kaushikk@vmware.com>
-   Removing netstat and replacing with ip route.
*   Tue Aug 11 2015 Kumar Kaushik <kaushikk@vmware.com>
-   VCA initial password issue fix.
*   Thu Jun 25 2015 Kumar Kaushik <kaushikk@vmware.com>
-   Removing systemd-service.patch. No longer needed.
*   Thu Jun 18 2015 Vinay Kulkarni <kulkarniv@vmware.com>
-   Add patch to enable logging to /var/log/cloud-init.log
*   Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com>
-   Update according to UsrMove.
*   Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-   Initial packaging for Photon
