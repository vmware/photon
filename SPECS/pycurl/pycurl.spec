%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           pycurl
Version:        7.19.5.1
Release:	    1
Summary:        A Python interface to libcurl
Group:          Development/Languages
License:        LGPLv2+ and an MIT/X
URL:            http://pycurl.sourceforge.net/
Source0:        http://pycurl.sourceforge.net/download/pycurl-%{version}.tar.gz
Vendor:		VMware, Inc.
Distribution:	Photon
Provides:	pycurl
Requires:	python2
BuildRequires:	openssl-devel
BuildRequires:	python2-devel
BuildRequires:	python2-libs
BuildRequires: 	curl
Requires: 	curl
%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%prep
%setup -q -n pycurl-%{version}
rm -f doc/*.xml_validity
chmod a-x examples/*

%build
CFLAGS="$RPM_OPT_FLAGS -DHAVE_CURL_OPENSSL" python setup.py build

%install
rm -rf %{buildroot}
python setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/pycurl
chmod 755 %{buildroot}%{python_sitelib}/pycurl.so

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING-LGPL COPYING-MIT RELEASE-NOTES.rst ChangeLog README.rst examples doc tests
%{python_sitelib}/*

%changelog
*	Sat Jan 24 2015 Touseef Liaqat <tliaqat@vmware.com> 7.19.5.1
-	Initial build.	First version
