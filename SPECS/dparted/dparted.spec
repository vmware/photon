Summary:	My summary.
Name:		dparted
Version:	0.1
Release:	1
License:	GPLv2+
URL:		dparted-0.1.tar.gz
Group:		Applications/System
Vendor:		VMware, Inc.
Distribution:	Photon
Source0:	%{name}-%{version}.tar.gz
Requires:	python2 >= 2.7
BuildRequires:	parted
BuildRequires:	glibmm
BuildRequires:	intltool
BuildRequires:	XML-Parser
BuildRequires:	glib-devel
Requires:	glib
Requires:	parted
Requires:	glibmm
%description
My lib
%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--disable-doc \
	--disable-scrollkeeper \
	--disable-nls
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files 
%defattr(-,root,root)
%{_sbindir}/*
%{_datadir}/*
%changelog
*	Thu Nov 12 2014 Mahmoud Bassiouny <mbassiouny@vmware.com> 0.18.0-1
	Initial version
