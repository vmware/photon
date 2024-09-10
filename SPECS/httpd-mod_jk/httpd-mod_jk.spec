Summary:        Apache Tomcat Connector
Name:           httpd-mod_jk
Version:        1.2.48
Release:        14%{?dist}
License:        Apache
URL:            http://tomcat.apache.org/connectors-doc
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://www.apache.org/dist/tomcat/tomcat-connectors/jk/tomcat-connectors-%{version}-src.tar.gz
%define sha512 tomcat-connectors=955a830724a3902e29032a5d2e7603d3170334e8a383d314f6bf8539d53d9f7ee4cfa0b31cfc954acb0a13d9975ed2229de085d08de3885f8679b509924fde47

Requires: httpd

BuildRequires: apr-devel
BuildRequires: apr-util-devel
BuildRequires: httpd-devel
BuildRequires: httpd-tools

%description
The Apache Tomcat Connectors project is part of the Tomcat project and provides web server plugins to connect web servers with Tomcat and other backends.
mod_jk is a module connecting Tomcat and Apache

%prep
%autosetup -n tomcat-connectors-%{version}-src -p1

%build
cd native
sh ./configure --with-apxs=%{_bindir}/apxs

make %{?_smp_mflags}

%install
install -vdm 755 %{buildroot}
install -D -m 755 native/apache-2.0/mod_jk.so %{buildroot}%{_libdir}/httpd/modules/mod_jk.so
install -D -m 644 conf/workers.properties  %{buildroot}%{_sysconfdir}/httpd/conf/workers.properties
install -D -m 644 conf/httpd-jk.conf  %{buildroot}%{_sysconfdir}/httpd/conf/httpd_jk.conf

%check
make -k check %{?_smp_mflags} |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root)
%{_libdir}/httpd/modules/mod_jk.so
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd_jk.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/workers.properties

%changelog
* Tue Sep 10 2024 Kuntal Nayak <kuntal.nayak@broadcom.com> 1.2.48-14
- Bump version as a part of apr upgrade
* Tue Jul 23 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.2.48-13
- Version Bump up to consume httpd v2.4.62
* Tue Jul 09 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.2.48-12
- Version Bump up to consume httpd v2.4.61
* Fri Apr 05 2024 Nitesh Kumar <nitesh-nk.kumar@broadcom.com> 1.2.48-11
- Version Bump up to consume httpd v2.4.59
* Mon Oct 30 2023 Nitesh Kumar <kunitesh@vmware.com> 1.2.48-10
- Bump version as a part of httpd v2.4.58 upgrade
* Fri Sep 29 2023 Nitesh Kumar <kunitesh@vmware.com> 1.2.48-9
- Bump version as a part of apr-util v1.6.3 upgrade
* Fri May 19 2023 Srish Srinivasan <ssrish@vmware.com> 1.2.48-8
- Bump version as a part of apr version upgrade
* Mon Apr 03 2023 Nitesh Kumar <kunitesh@vmware.com> 1.2.48-7
- Bump version as a part of httpd v2.4.56 upgrade
* Mon Jan 30 2023 Nitesh Kumar <kunitesh@vmware.com> 1.2.48-6
- Bump version as a part of httpd v2.4.55 upgrade
* Mon Jun 20 2022 Nitesh Kumar <kunitesh@vmware.com> 1.2.48-5
- Bump version as a part of httpd v2.4.54 upgrade
* Tue Oct 19 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.2.48-4
- Bump version as a part of httpd upgrade
* Thu Oct 07 2021 Dweep Advani <dadvani@vmware.com> 1.2.48-3
- Rebuild with upgraded httpd 2.4.50
* Tue Oct 05 2021 Shreenidhi Shedi <sshedi@vmware.com> 1.2.48-2
- Bump version as a part of httpd upgrade
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 1.2.48-1
- Automatic Version Bump
* Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 1.2.44-1
- Upgrade to latest version
* Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.42-2
- Ensure non empty debuginfo
* Tue Feb 21 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.2.42-1
- Initial build. First version
