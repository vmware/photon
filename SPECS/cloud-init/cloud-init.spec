Name:           cloud-init
Version:        0.7.9
Release:        1%{?dist}
Summary:        Cloud instance init scripts
Group:          System Environment/Base
License:        GPLv3
URL:            http://launchpad.net/cloud-init
Source0:        https://launchpad.net/cloud-init/trunk/%{version}/+download/%{name}-%{version}.tar.gz
%define sha1 cloud-init=3b4345267e72e28b877e2e3f0735c1f672674cfc
Source1:        cloud-photon.cfg

Patch0:         photon-distro.patch
Patch1:         change-requires.patch
Patch2:         vca-admin-pwd.patch
Patch3:         photon-hosts-template.patch
Patch4:         resizePartitionUUID.patch
Patch5:         datasource-guestinfo.patch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  systemd
BuildRequires:  dbus
BuildRequires:  python-ipaddr
BuildRequires:  iproute2
BuildRequires:  automake

Requires:       systemd
Requires:       net-tools
Requires:       python2
Requires:       python2-libs
Requires:       python-configobj
Requires:       python-prettytable
Requires:       python-requests
Requires:       python-setuptools
Requires:       PyYAML
Requires:       python-jsonpatch
Requires:       python-jinja2
Requires:       python-oauthlib
Requires:       python-markupsafe
Requires:       python-six

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

find systemd -name cloud*.service | xargs sed -i s/StandardOutput=journal+console/StandardOutput=journal/g

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT --init-system systemd

# Don't ship the tests
rm -r $RPM_BUILD_ROOT%{python_sitelib}/tests

mkdir -p $RPM_BUILD_ROOT/var/lib/cloud

# We supply our own config file since our software differs from Ubuntu's.
cp -p %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/cloud/cloud.cfg

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
%{_sysconfdir}/NetworkManager/dispatcher.d/hook-network-manager
%{_sysconfdir}/dhcp/dhclient-exit-hooks.d/hook-dhclient
/lib/systemd/system-generators/cloud-init-generator
/lib/udev/rules.d/66-azure-ephemeral.rules
/lib/systemd/system/*
%{_docdir}/cloud-init/*
%{_libdir}/cloud-init/*
%{python_sitelib}/*
%{_bindir}/cloud-init*
%dir /var/lib/cloud


%changelog
*   Thu Apr 13 2017 Anish Swaminathan <anishs@vmware.com> 0.7.9-1
-   Upgraded to version 0.7.9
-   Enabled VmxGuestinfo datasource
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
