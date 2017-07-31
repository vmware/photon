Summary:	Logrotate
Name:		logrotate
Version:	3.11.0
Release:	3%{?dist}
License:	GPL+
URL:		https://github.com/logrotate/logrotate/
Source0:	https://github.com/logrotate/logrotate/archive/%{name}-%{version}.tar.gz
%define sha1 logrotate=baeb2676edbfffb04a567e5b1a61e4e19cfc50f4
Group:		System Environment/Base
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	popt-devel
Requires:	popt
%description
The logrotate utility is designed to simplify the administration of log files on a system which generates a lot of log files. Logrotate allows for the automatic rotation compression, removal and mailing of log files. Logrotate can be set to handle a log file daily, weekly, monthly or when the log file gets to a certain size.
%prep
%setup -q
%build
./autogen.sh
./configure \
	--prefix=%{_prefix}
# logrotate code has misleading identation and GCC 6.3 does not like it.
make %{?_smp_mflags} CFLAGS="-Wno-error=misleading-indentation -g -O2"

%install
make DESTDIR=%{buildroot} install
install -vd %{buildroot}%{_sysconfdir}/logrotate.d
install -p -m 644 examples/logrotate-default %{buildroot}%{_sysconfdir}/logrotate.conf
install -vd %{buildroot}%{_sysconfdir}/cron.daily
install -p -m 755 examples/logrotate.cron %{buildroot}%{_sysconfdir}/cron.daily/logrotate
install -vd %{buildroot}%{_localstatedir}/lib/logrotate
touch %{buildroot}%{_localstatedir}/lib/logrotate/logrotate.status

%post
/sbin/ldconfig

if [ $1 -eq 1 ];then
    # This is initial installation
    mkdir -p -m 755 /etc/logrotate.d
fi

%postun
/sbin/ldconfig

if [ $1 -eq 0 ];then
    # This is erase operation
    rm -rf /etc/logrotate.d
fi

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/cron.daily/logrotate
%config(noreplace) %{_sysconfdir}/logrotate.conf
%{_sbindir}/logrotate
%{_mandir}/man5/logrotate.conf.5.gz
%{_mandir}/man8/logrotate.8.gz
/var/lib/logrotate/logrotate.status

%changelog
*       Mon Jul 31 2017 Kumar Kaushik <kaushikk@vmware.com> 3.11.0-3
-       Creating /etc/logrotate.d folder as part of package installation, Bug#1878180.
*       Wed Jun 14 2017 Anish Swaminathan <anishs@vmware.com> 3.11.0-2
-       Mark config files as noreplace
*       Fri Apr 14 2017 Kumar Kaushik <kaushikk@vmware.com> 3.11.0-1
-       Updating version to 3.11.0
*	Mon Mar 13 2017 Alexey Makhalov <amakhalov@vmware.com> 3.9.1-3
-	Compilation for gcc 6.3
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.9.1-2
-	GA - Bump release of all rpms
*	Wed Jun 24 2015 Divya Thaluru <dthaluru@vmware.com> 3.9.1-1
-	Initial build. First version

