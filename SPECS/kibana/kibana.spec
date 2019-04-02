Name:            kibana
Summary:         Browser-based analytics and search dashboard for Elasticsearch.
Version:         6.7.0
Release:         1%{?dist}
License:         Apache License Version 2.0
URL:             https://www.elastic.co/products/kibana
Source0:         https://github.com/elastic/kibana/archive/%{name}-%{version}.tar.gz
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           System Environment/Daemons
%define sha1     %{name}-%{version}=36bc3dea07c787c395d1b6aaf46e2ade93c5b7a9
BuildRequires:   git
BuildRequires:   yarn
BuildRequires:   nodejs10
BuildRequires:   zip
BuildRequires:   photon-release
BuildRequires:   systemd
Requires:        systemd
Requires:        nodejs10
Requires:        elasticsearch

%global debug_package %{nil}

%description
Kibana is a window into the Elastic Stack.
It enables visual exploration and real-time analysis of your data in Elasticsearch.

%prep
# During building, it looks .git/hooks in the root path
# But tar.gz file  from github/kibana/tag doesn't provide .git/hooks
# inside it. so did below steps to create the tar
# 1) git clone https://github.com/elastic/kibana.git kibana-%{version}
# 2) cd kibana-%{version}
# 3) git checkout tags/v6.7.0 -b 6.7.0
# 4) cd ..
# 5) tar -zcvf kibana-6.7.0.tar.gz kibana-%{version}
%setup -q -n %{name}-%{version}

yarn kbn bootstrap

%build
export PATH=${PATH}:/usr/bin
yarn build --oss --skip-os-packages

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -r build/kibana-oss/LICENSE.txt %{buildroot}%{_datadir}/%{name}
cp -r build/kibana-oss/README.txt %{buildroot}%{_datadir}/%{name}
cp -r build/kibana-oss/NOTICE.txt %{buildroot}%{_datadir}/%{name}
cp -r build/kibana-oss/package.json %{buildroot}%{_datadir}/%{name}
cp -r build/kibana-oss/plugins %{buildroot}%{_datadir}/%{name}
cp -r build/kibana-oss/bin %{buildroot}%{_datadir}/%{name}
cp -r build/kibana-oss/src %{buildroot}%{_datadir}/%{name}
cp -r build/kibana-oss/node_modules %{buildroot}%{_datadir}/%{name}
cp -r build/kibana-oss/webpackShims %{buildroot}%{_datadir}/%{name}
cp -r build/kibana-oss/optimize %{buildroot}%{_datadir}/%{name}

chmod -R 755 %{buildroot}%{_datadir}/%{name}

install -vdm 755 %{buildroot}%{_sharedstatedir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/default
install -D -m 644 src/dev/build/tasks/os_packages/service_templates/sysv/etc/default/kibana %{buildroot}%{_sysconfdir}/default

mkdir -p %{buildroot}%{_sysconfdir}/systemd/system
install -D -m 644 src/dev/build/tasks/os_packages/service_templates/systemd/etc/systemd/system/kibana.service %{buildroot}%{_sysconfdir}/systemd/system

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -D -m 644 config/%{name}.yml %{buildroot}%{_sysconfdir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/init.d
install -D -m 644 src/dev/build/tasks/os_packages/service_templates/sysv/etc/init.d/%{name} %{buildroot}%{_sysconfdir}/init.d

rm -rf %{buildroot}%{_datadir}/%{name}/node_modules/clipboardy

%pre -p /bin/sh
if ! getent group %{name} >/dev/null; then
    groupadd -r %{name}
fi
if ! getent passwd %{name} >/dev/null; then
    useradd -r -g %{name} -d /var/lib/%{name} -s /sbin/nologin  -c "Kibana User" %{name}
fi
exit 0


%post
/sbin/ldconfig
chown -R kibana:kibana /var/lib/kibana
chown -R kibana:kibana /usr/share/kibana
%systemd_post  %{name}.service

%preun
/sbin/ldconfig
%systemd_preun %{name}.service

%postun -p /bin/sh
%systemd_postun_with_restart %{name}.service
if [ $1 -eq 0 ] ; then
   getent passwd kibana > /dev/null
   if [ "$?" == "0" ] ; then
      userdel %{name}
   fi
   getent group kibana >/dev/null
   if [ "$?" == "0" ] ; then
      groupdel %{name}
   fi
fi
exit

%files
%defattr(-,root,root,-)
%dir %{_sharedstatedir}/%{name}
%doc %{_datadir}/%{name}/LICENSE.txt
%doc %{_datadir}/%{name}/README.txt
%{_sysconfdir}/systemd/system/%{name}.service
%{_sysconfdir}/default/%{name}
%{_sysconfdir}/init.d/%{name}
%{_sysconfdir}/%{name}/%{name}.yml
%{_datadir}/%{name}/package.json
%dir %{_datadir}/%{name}
%{_datadir}/%{name}

%changelog
*   Tue Apr 02 2019 Ankit Jain <ankitja@vmware.com> 6.7.0-1
-   Updated to version 6.7.0
*   Mon Apr 01 2019 Siju Maliakkal <smaliakkal@vmware.com> 6.4.3-2
-   Applied Patch for CVE-2019-7609
*   Wed Feb 13 2019 Siju Maliakkal <smaliakkal@vmware.com> 6.4.3-1
-   Upgrade to 6.4.3 CVE-2018-17245,CVE-2018-17246
*   Wed Jan 23 2019 Siju Maliakkal <smaliakkal@vmware.com> 6.4.1-1
-   Upgrade to 6.4.1 to mitigate CVE-2018-3830
*   Tue Sep 11 2018 Keerthana K <keerthanak@vmware.com> 6.4.0-1
-   Updated to version 6.4.0
*   Mon Jul 09 2018 Keerthana K <keerthanak@vmware.com> 6.3.0-1
-   Initial kibana package for PhotonOS.
