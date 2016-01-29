%define debug_package %{nil}
Summary:	The Sysstat package contains utilities to monitor system performance and usage activity
Name:		sysstat 
Version:	11.2.0
Release:	1%{?dist}
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
            --disable-file-attr &&
make %{?_smp_mflags}
%install
make install
mv %{buildroot}/usr/lib64  %{buildroot}/%{_libdir}

%clean
rm -rf %{buildroot}/*

%files 
%defattr(-,root,root)
%{_sysconfdir}
%{_bindir}
%{_datadir}
%{_libdir}

%changelog
*	Wed Jan 20 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 11.2.0-1
-	Update to 11.2.0-1.
*	Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 11.1.8-1
-	Initial build.	First version
