Name:            kibana
Summary:         Browser-based analytics and search dashboard for Elasticsearch.
Version:         6.8.15
Release:         1%{?dist}
License:         Apache License Version 2.0
URL:             https://www.elastic.co/products/kibana
Source0:         https://github.com/elastic/kibana/archive/%{name}-%{version}.tar.gz
Vendor:          VMware, Inc.
Distribution:    Photon
Group:           System Environment/Daemons
%define sha1     %{name}-%{version}=68bf9762c769b31535ddd91c8ec0a8a4efc8ea51
Source1:         kibana_build-%{version}.tar.gz
%define sha1     kibana_build-%{version}=fc21e7454f1de22f6b84ba0aac5c95759125e263
BuildRequires:   git
BuildRequires:   yarn
BuildRequires:   nodejs10
BuildRequires:   zip
BuildRequires:   photon-release
BuildRequires:   systemd
Requires:        systemd
Requires:        nodejs
Requires:        elasticsearch = %{version}

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


%build

export PATH=${PATH}:/usr/bin
#For building kibana pls, follow the below commands.

#this command will download all the required node modules
#yarn kbn bootstrap

#this command will do the build
#yarn build --oss --skip-os-packages

tar xf %{SOURCE1} --no-same-owner

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -r build/oss/%{name}-%{version}-SNAPSHOT-linux-x86_64/LICENSE.txt %{buildroot}%{_datadir}/%{name}
cp -r build/oss/%{name}-%{version}-SNAPSHOT-linux-x86_64/README.txt %{buildroot}%{_datadir}/%{name}
cp -r build/oss/%{name}-%{version}-SNAPSHOT-linux-x86_64/NOTICE.txt %{buildroot}%{_datadir}/%{name}
cp -r build/oss/%{name}-%{version}-SNAPSHOT-linux-x86_64/package.json %{buildroot}%{_datadir}/%{name}
cp -r build/oss/%{name}-%{version}-SNAPSHOT-linux-x86_64/plugins %{buildroot}%{_datadir}/%{name}
cp -r build/oss/%{name}-%{version}-SNAPSHOT-linux-x86_64/bin %{buildroot}%{_datadir}/%{name}
cp -r build/oss/%{name}-%{version}-SNAPSHOT-linux-x86_64/src %{buildroot}%{_datadir}/%{name}
cp -r build/oss/%{name}-%{version}-SNAPSHOT-linux-x86_64/node_modules %{buildroot}%{_datadir}/%{name}
cp -r build/oss/%{name}-%{version}-SNAPSHOT-linux-x86_64/webpackShims %{buildroot}%{_datadir}/%{name}
cp -r build/oss/%{name}-%{version}-SNAPSHOT-linux-x86_64/optimize %{buildroot}%{_datadir}/%{name}
cp -r build/oss/%{name}-%{version}-SNAPSHOT-linux-x86_64/node %{buildroot}%{_datadir}/%{name}
cp -r build/oss/%{name}-%{version}-SNAPSHOT-linux-x86_64/built_assets %{buildroot}%{_datadir}/%{name}
cp -r build/oss/%{name}-%{version}-SNAPSHOT-linux-x86_64/target %{buildroot}%{_datadir}/%{name}

chmod -R 755 %{buildroot}%{_datadir}/%{name}

install -vdm 755 %{buildroot}%{_sharedstatedir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/default
install -D -m 644 src/dev/build/tasks/os_packages/service_templates/sysv/etc/default/kibana %{buildroot}%{_sysconfdir}/default

mkdir -p %{buildroot}%{_sysconfdir}/systemd/system
install -D -m 644 src/dev/build/tasks/os_packages/service_templates/systemd/etc/systemd/system/kibana.service %{buildroot}%{_sysconfdir}/systemd/system

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -D -m 644 config/%{name}.yml %{buildroot}%{_sysconfdir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
install -D -m 644 src/dev/build/tasks/os_packages/service_templates/sysv/etc/init.d/%{name} %{buildroot}%{_sysconfdir}/rc.d/init.d

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
%{_sysconfdir}/rc.d/init.d/%{name}
%{_sysconfdir}/%{name}/%{name}.yml
%{_datadir}/%{name}/package.json
%dir %{_datadir}/%{name}
%{_datadir}/%{name}

%changelog
*   Wed Apr 07 2021 Piyush Gupta <gpiyush@vmware.com> 6.8.15-1
-   Update to 6.8.15
*   Tue Mar 16 2021 Piyush Gupta <gpiyush@vmware.com> 6.8.13-2
-   Release bump up with new nodejs.
*   Wed Nov 18 2020 Piyush Gupta <gpiyush@vmware.com> 6.8.13-1
-   Upgrade to 6.8.13, Fix for CVE-2020-7020
*   Wed Oct 07 2020 Piyush Gupta <gpiyush@vmware.com> 6.8.12-2
-   Release bump up for CVE-2020-8252
*   Mon Aug 31 2020 Piyush Gupta <gpiyush@vmware.com> 6.8.12-1
-   Update to release 6.8.12
*   Thu Jun 18 2020 Tapas Kundu <tkundu@vmware.com> 6.8.10-1
-   Update to release 6.8.10
*   Tue May 05 2020 Tapas Kundu <<tkundu@vmware.com> 6.8.9-1
-   Update to release 6.8.9
*   Wed Oct 09 2019 Tapas Kundu <tkundu@vmware.com> 6.7.0-3
-   Use bundled source to build
*   Thu Jul 18 2019 Sujay G <gsujay@vmware.com> 6.7.0-2
-   Added missing dll's & config files
-   Packaged file from the correct oss build folder
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
