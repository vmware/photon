%global __requires_exclude perl\\(.*\\)
Summary:        Net-SNMP is a suite of applications used to implement SNMP v1, SNMP v2c and SNMP v3 using both IPv4 and IPv6.
Name:           net-snmp
Version:        5.8
Release:        1%{?dist}
License:        BSD (like)
URL:            http://net-snmp.sourceforge.net/
Group:          Productivity/Networking/Other
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{name}-%{version}.tar.gz
%define sha1 net-snmp=78f70731df9dcdb13fe8f60eb7d80d7583da4d2c
Source1:        snmpd.service
Source2:        snmptrapd.service
Patch0:         net-snmp-CVE-2019-20892.patch
Patch1:         net-snmp-5.8-CVE-2020-15861.patch
Patch2:         net-snmp-5.8-CVE-2020-15862.patch

BuildRequires:  openssl-devel
BuildRequires:  perl
BuildRequires:  systemd
Requires:       perl
Requires:       systemd
%description
 Net-SNMP is a suite of applications used to implement SNMP v1, SNMP v2c and SNMP v3 using both IPv4 and IPv6.

%package devel
Group: Development/Libraries
Summary: The includes and static libraries from the Net-SNMP package.
Requires: net-snmp = %{version}-%{release}

%description devel
The net-snmp-devel package contains headers and libraries for building SNMP applications.

%prep
%autosetup -p1

%build
%configure \
                --host=ia64-linux \
                --build=i686 \
                --target=ia64-linux \
                --sbindir=/sbin \
                --with-sys-location="unknown" \
                --with-logfile=/var/log/net-snmpd.log \
                --with-persistent-directory=/var/lib/net-snmp \
                --with-sys-contact="root@localhost" \
                --with-defaults \
                --with-systemd \
                --disable-static \
                --with-x=no \
                --enable-as-needed

make %{?_smp_mflags}

%install
make install %{?_smp_mflags} DESTDIR=%{buildroot}
mkdir -p %{buildroot}/lib/systemd/system
install -m 0644 %{SOURCE1} %{buildroot}/lib/systemd/system/snmpd.service
install -m 0644 %{SOURCE2} %{buildroot}/lib/systemd/system/snmptrapd.service

#Delete unnecessary stuff
find %{buildroot}/%{_libdir}/perl5/ -name Bundle -type d | xargs rm -rf
find %{buildroot}/%{_libdir}/perl5/ -name perllocal.pod | xargs rm -f

# store a copy of installed Perl stuff.
# This is based off the netsnmp github repo - https://github.com/net-snmp/net-snmp/blob/master/dist/net-snmp.spec
(xxdir=`pwd` && cd %{buildroot} && find usr/lib*/perl5 -type f | sed 's/^/\//' > $xxdir/net-snmp-perl-files)

%check
make %{?_smp_mflags} test

%post
if [ $1 == 2 ]; then
  # Upgrading net-snmp, preserve the existing config in /usr/etc/snmp
  if [ -d /usr/etc/snmp -a ! -e %{_sysconfdir}/snmp ]; then
    ln -sf /usr/etc/snmp %{_sysconfdir}/snmp
  fi
fi
/sbin/ldconfig
%systemd_post snmpd.service
%systemd_post snmptrapd.service

%preun
%systemd_preun snmpd.service
%systemd_preun snmptrapd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart snmpd.service
%systemd_postun_with_restart snmptrapd.service

%clean
rm -rf %{buildroot}/*

%files
%doc COPYING NEWS README ChangeLog
%defattr(-,root,root)
/lib/systemd/system/snmpd.service
/lib/systemd/system/snmptrapd.service
%{_bindir}
%{_libdir}/*.so.*
/sbin/*
%ghost %config(noreplace) %{_sysconfdir}/snmp
%{_datadir}/snmp/snmpconf-data/
%{_datadir}/snmp/snmp_perl.pl
%{_datadir}/snmp/snmp_perl_trapd.pl
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root)
%{_includedir}
%{_libdir}/*.la
%{_libdir}/perl5
%{_libdir}/*.so
%{_datadir}/snmp/mibs
%{_datadir}/snmp/mib2c*
%{_mandir}/man3/*

%changelog
*   Tue Jun 29 2021 Shreenidhi Shedi <sshedi@vmware.com> 5.8-1
-   Bump to 5.8 as a part of RPM upgrade
*   Thu Aug 27 2020 Shreyas B. <shreyasb@vmware.com> 5.7.3-15
-   Fix for CVE-2020-15861 & CVE-2020-15862
*   Tue Jul 07 2020 Shreyas B. <shreyasb@vmware.com> 5.7.3-14
-   Fix for CVE-2019-20892
*   Mon Jan 13 2020 Ankit Jain <ankitja@vmware.com> 5.7.3-13
-   Moved snmpconf-data files to base pkg to
-   fix "snmpconf -g basic_setup"
*   Mon Jan 13 2020 Ankit Jain <ankitja@vmware.com> 5.7.3-12
-   Added release number in Requires of devel
*   Wed Feb 20 2019 Dweep Advani <dadvani@vmware.com> 5.7.3-11
-   Fixed snmpd.conf path
*   Mon Dec 31 2018 Ankit Jain <ankitja@vmware.com> 5.7.3-10
-   Fix for CVE-2018-18065
*   Tue Jul 31 2018 Ajay Kaher <akaher@vmware.com> 5.7.3-9
-   Excluded perllocal.pod for aarch64
*   Mon Apr 16 2018 Xiaolin Li <xiaolinl@vmware.com> 5.7.3-8
-   Apply patch for CVE-2018-1000116
*   Mon Jul 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 5.7.3-7
-   Make service file a different source
*   Tue Apr 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.7.3-6
-   Patch to remove U64 typedef
*   Tue Oct 04 2016 ChangLee <changLee@vmware.com> 5.7.3-5
-   Modified %check
*   Thu May 26 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 5.7.3-4
-   Excluded the perllocal.pod log.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.7.3-3
-   GA - Bump release of all rpms
*   Wed May 04 2016 Nick Shi <nshi@vmware.com> 5.7.3-2
-   Add snmpd and snmptrapd to systemd service.
*   Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 5.7.3-1
-   Initial build.  First version
