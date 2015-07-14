Summary:	libnfsidmap
Name:		libnfsidmap
Version:	0.25
Release:	1
License:	GPLv3+
URL:		http://www.linuxfromscratch.org/
Group:		Applications/libnfsidmap
Source0:	%{name}-%{version}.tar.gz
Vendor:		VMware, Inc.
Distribution:	Photon

%description
The libnfsidmap package support nfsv4 nfs service

%prep
%setup -q
%configure --prefix=%{_prefix}
%build
make %{?_smp_mflags}
%install
make   DESTDIR=%{buildroot} install


%files
%define _missing_doc_files_terminate_build 0 
%defattr(-,root,root)
%{_libdir}/*
%{_includedir}/*
%{_datadir}/*
%changelog
*	Sat Jul 4 2015 Rongrong Qiu <rqiu@vmware.com> 0.25-1
-	Initial build.	First version
