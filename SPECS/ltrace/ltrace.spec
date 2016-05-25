Summary:	ltrace intercepts and records dynamic library calls.
Name:		ltrace
Version:	0.7.3
Release:	2%{?dist}
License:	GPLv2+
URL:		http://www.ltrace.org/
Group:		Development/Debuggers
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	http://www.ltrace.org/%{name}_%{version}.orig.tar.bz2
%define sha1 ltrace=8df2acc8bc135a229917de6ef814f416d38124ca
BuildRequires:	elfutils-libelf-devel
Requires:	elfutils-libelf
%description
ltrace intercepts and records dynamic library calls which are called by an executed process and the signals received by that process. It can also intercept and print the system calls executed by the program.

%prep
%setup -q
%build

./configure \
	--prefix=%{_prefix} --disable-werror 

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
make -k check 

%clean
rm -rf %{buildroot}/*

%files 
%defattr(-,root,root)
/usr/etc/ltrace.conf
%{_bindir}/*
%{_datadir}
%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 	0.7.3-2
-	GA - Bump release of all rpms
*	Wed Nov 25 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 0.7.3-1
-	Initial build.	First version
