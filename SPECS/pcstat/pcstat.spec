Summary:	A tool that inspect which pages of a file or files are being cached by the Linux kernel
Name:		pcstat 
Version:	1
Release:	2%{?dist}
License:	Apache 
URL:		https://github.com/tobert/pcstat
Group:		Development/Debuggers
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	https://github.com/tobert/pcstat/archive/pcstat-1.zip
%define sha1 pcstat=cd67c42d291763597dbe3fb19e8e367c54a4a898
BuildRequires:	unzip go audit git
Requires:	go
%description
A tool that inspect which pages of a file or files are being cached by the Linux kernel

%prep
%setup -qn pcstat-master
%build
go get golang.org/x/sys/unix
go build

%install
mkdir -p %{buildroot}/usr/local/bin
cp -a pcstat %{buildroot}/usr/local/bin

%clean
rm -rf %{buildroot}/*

%files 
%defattr(-,root,root)
/usr/local/bin

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	1-2
-	GA - Bump release of all rpms
*	Wed Nov 25 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.7.3-1
-	Initial build.	First version
