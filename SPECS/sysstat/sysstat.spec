Summary:	The Sysstat package contains utilities to monitor system performance and usage activity
Name:		sysstat 
Version:	11.1.8
Release:	1%{?dist}
License:	GPLv2 
URL:		http://sebastien.godard.pagesperso-orange.fr/
Group:		Development/Debuggers
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://perso.wanadoo.fr/sebastien.godard/sysstat-11.1.8.tar.xz
%define sha1 sysstat=2da5098c4d6626a85821d943ab3299b003c39f4e

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
*	Mon Nov 30 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 11.1.8-1
-	Initial build.	First version
