# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

Summary:	The Sysstat package contains utilities to monitor system performance and usage activity
Name:		sysstat 
Version:	11.2.0
Release:	3%{?dist}
License:	GPLv2 
URL:		http://sebastien.godard.pagesperso-orange.fr/
Group:		Development/Debuggers
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://perso.wanadoo.fr/sebastien.godard/sysstat-11.2.0.tar.xz
%define sha1 sysstat=61b70892d864f8bac5714e2fe0a006f0fda6efba
%description
 The Sysstat package contains utilities to monitor system performance and usage activity. Sysstat contains the sar utility, common to many commercial Unixes, and tools you can schedule via cron to collect and historize performance and activity data. 

%prep
%setup -q
%build

./configure --prefix=%{_prefix} \
            --disable-file-attr \
            sa_lib_dir=%{_libdir}/sa \
	    --mandir=%{_mandir}
make %{?_smp_mflags}
%install
make install
mkdir -p %{buildroot}/usr/lib/systemd/system/
install -D -m 0644 %{_builddir}/%{name}-%{version}/sysstat.service %{buildroot}/usr/lib/systemd/system/
%clean
rm -rf %{buildroot}/*

%files 
%defattr(-,root,root)
%{_sysconfdir}/*
%{_bindir}/*
%{_libdir}/sa/*
%{_datadir}/doc/%{name}-%{version}/*
%{_datadir}/locale/*/LC_MESSAGES/sysstat.mo
%{_mandir}/man*/*
%{_libdir}/systemd/system/*


%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 11.2.0-3
-	GA - Bump release of all rpms
*	Wed May 4 2016 Divya Thaluru <dthaluru@vmware.com> 11.2.0-2
-	Adding systemd service file
*	Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 11.2.0-1
-	Update to 11.2.0-1.
*	Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 11.1.8-1
-	Initial build.	First version
