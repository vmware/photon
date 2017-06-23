Summary:	Netcat is a featured networking utility which reads and writes data across network connections, using the TCP/IP protocol.
Name:		netcat
Version:	0.7.1
Release:	3%{?dist}
License:	GPLv2 
URL:		http://netcat.sourceforge.net/
Group:		Productivity/Networking/Other
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://downloads.sourceforge.net/project/%{name}/%{name}/0.7.1/%{name}-%{version}.tar.gz
%define sha1 netcat=b5cbc52a7ceed2fd5c4f5081f5747130b2d0fe01

%description
Netcat is a featured networking utility which reads and writes data across network connections, using the TCP/IP protocol.
It is designed to be a reliable "back-end" tool that can be used directly or easily driven by other programs and scripts. At the same time, it is a feature-rich network debugging and exploration tool, since it can create almost any kind of connection you would need and has several interesting built-in capabilities.

%prep
%setup -q
%build

./configure --prefix=%{_prefix} 
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%{_bindir}
/usr/info/
%{_datadir}
/usr/man
%changelog
*   Fri Jun 23 2017 Divya Thaluru <dthaluru@vmware.com> 0.7.1-3
-   Removed packaging of debug files
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.7.1-2
-   GA - Bump release of all rpms
*   Tue Dec 08 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.7.1-1
-   Initial build.	First version
