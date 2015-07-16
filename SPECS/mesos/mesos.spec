Summary:	Mesos
Name:		mesos
Version:	0.22.1
Release:	1%{?dist}
License:	Apache
URL:		http://mesos.apache.org
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	http://apache.mirrors.lucidnetworks.net/mesos/%{name}-%{version}.tar.gz
Requires:	openjdk >= 1.8.0.45
Requires:	expat
BuildRequires:	openjdk >= 1.8.0.45
BuildRequires:	curl
BuildRequires:	apache-maven >= 3.3.3
BuildRequires:	apr >= 1.5.2
BuildRequires:	apr-util >= 1.5.4
BuildRequires:	subversion >= 1.8.13
BuildRequires:	cyrus-sasl >= 2.1.26
BuildRequires:	python2 >= 2.6
BuildRequires:	python2-libs
BuildRequires:	python2-devel

%description
The Mesos package installs MesosContainerizer.

%prep

%setup -q
%build
./configure	--prefix=%{_prefix}  	

make %{?_smp_mflags}

%check
make check

%install
make DESTDIR=%{buildroot} install

[ %{buildroot} != "/"] && rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*
%{_includedir}/*/*
%{_sbindir}/*
%{_prefix}/etc/mesos/*
%{_libexecdir}/mesos/*
%{_datadir}/mesos/*

%changelog
*	Fri Jun 26 2015 Sarah Choi <sarahc@vmware.com> 0.22.1-1
-	Initial build.	First version
