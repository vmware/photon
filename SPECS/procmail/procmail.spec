Summary:	Autonomous Mail Processor
Name:		procmail
Version:	3.22
Release:	1%{?dist}
License:	GPLv2+
URL:		http://www.procmail.org
Group:		Applications/Internet
Source0:	http://www.ring.gr.jp/archives/net/mail/procmail/%{name}-%{version}.tar.gz
%define sha1 procmail=cd4e44c15559816453fd60349e5a32289f6f2965
Patch0:		procmail-3.22-config.patch
Vendor:		VMware, Inc.
Distribution:	Photon
%description
Procmail is a program for filtering, sorting and storing email. It can be used both on mail clients and mail servers. It can be used to filter out spam, checking for viruses, to send automatic replies, etc.
%prep
%setup -q
%patch0 -p1
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
*	Mon Nov 02 2015 Divya Thaluru <dthaluru@vmware.com> 3.22-1
-	Initial build.	First version
