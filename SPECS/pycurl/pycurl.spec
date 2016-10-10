%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           pycurl
Version:        7.21.5
Release:        4%{?dist}
Summary:        A Python interface to libcurl
Group:          Development/Languages
License:        LGPLv2+ and an MIT/X
URL:            http://pycurl.sourceforge.net/
Source0:        http://pycurl.sourceforge.net/download/pycurl-%{version}.tar.gz
%define sha1 pycurl=60865d22fc715ca5197117ea3ad32413d3c7402e
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

%package doc
Summary:	Documentation and examples for pycurl
Requires:	%{name} = %{version}

%description doc
Documentation and examples for pycurl

%prep
%setup -q -n pycurl-%{version}
rm -f doc/*.xml_validity
#chmod a-x examples/*

# removing prebuilt-binaries
rm -f tests/fake-curl/libcurl/*.so

%build
CFLAGS="$RPM_OPT_FLAGS -DHAVE_CURL_OPENSSL" python setup.py build

%install
rm -rf %{buildroot}
python setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/pycurl
chmod 755 %{buildroot}%{python_sitelib}/pycurl.so

%check
easy_install nose
easy_install bottle
easy_install flakey
sed -i 's/--with-flaky//g' tests/run.sh
make  %{?_smp_mflags} test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%files doc
%defattr(-,root,root)
%doc COPYING-LGPL COPYING-MIT RELEASE-NOTES.rst ChangeLog README.rst examples doc tests

%changelog
*       Mon Oct 10 2016 ChangLee <changlee@vmware.com> 7.21.5-4
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.21.5-3
-	GA - Bump release of all rpms
*	Fri Apr 29 2016 Divya Thaluru <dthaluru@vmware.com> 7.21.5-2
-	Removing prebuilt binaries
*	Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 7.21.5-1
-	Upgrade version
*	Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 7.19.5.1-2
-	Added Doc subpackage. Removed chmod a-x for examples.
*	Sat Jan 24 2015 Touseef Liaqat <tliaqat@vmware.com> 7.19.5.1
-	Initial build.	First version
