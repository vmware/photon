%{!?python_sitelib_platform: %define python_sitelib_platform %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: 	A fast metadata parser for yum
Name:       	yum-metadata-parser
Version:   	1.1.4
Release:    	2%{?dist}
Source0:    	%{name}-%{version}.tar.gz
%define sha1 yum-metadata-parser=044e69a04ea5ac39d79020d9e1f1a35c9dc64d9b
License:    	GPLv2+
Group:      	Development/Libraries
URL:        	http://devel.linux.duke.edu/cgi-bin/viewcvs.cgi/yum-metadata-parser/
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires: pkg-config
BuildRequires: python2-devel
BuildRequires: glib-devel
BuildRequires: libxml2
BuildRequires: libxml2-devel
BuildRequires: sqlite-autoconf
BuildRequires:	python2-libs
Requires:	libxml2
Requires:	glib
Requires:	python2
%description
Fast metadata parser for yum implemented in C.

%prep
%setup

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --root=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%{python_sitelib_platform}/_sqlitecache.so
%{python_sitelib_platform}/sqlitecachec.py
%{python_sitelib_platform}/sqlitecachec.pyc
%{python_sitelib_platform}/sqlitecachec.pyo
%{python_sitelib_platform}/*egg-info
