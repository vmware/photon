# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

Summary:	Autonomous Mail Processor
Name:		procmail
Version:	3.22
Release:	3%{?dist}
License:	GPLv2+
URL:		http://www.procmail.org
Group:		Applications/Internet
Source0:	http://www.ring.gr.jp/archives/net/mail/procmail/%{name}-%{version}.tar.gz
%define sha1 procmail=cd4e44c15559816453fd60349e5a32289f6f2965
Patch0:		procmail-3.22-config.patch
Patch1:		procmail-3.22-CVE-2014-3618.patch
Vendor:		VMware, Inc.
Distribution:	Photon
%description
Procmail is a program for filtering, sorting and storing email. It can be used both on mail clients and mail servers. It can be used to filter out spam, checking for viruses, to send automatic replies, etc.
%prep
%setup -q
%patch0 -p1
%patch1 -p1
%build
sed -i 's/getline/get_line/' src/*.[ch]

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man{1,5}
make BASENAME=%{buildroot}%{_prefix} MANDIR=${RPM_BUILD_ROOT}%{_mandir}  install
make BASENAME=%{buildroot}%{_prefix} install-suid

%files
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.22-3
-	GA - Bump release of all rpms
* 	Wed Mar 30 2016 Anish Swaminathan <anishs@vmware.com>  3.22-2
- 	Add patch for CVE-2014-3618
*	Mon Nov 02 2015 Divya Thaluru <dthaluru@vmware.com> 3.22-1
-	Initial build.	First version
