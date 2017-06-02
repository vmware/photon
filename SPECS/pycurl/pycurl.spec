%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Name:           pycurl
Version:        7.21.5
Release:        4%{?dist}
Summary:        A Python interface to libcurl
Group:          Development/Languages
License:        LGPLv2+ and an MIT/X
URL:            http://pycurl.sourceforge.net/
Source0:        http://pycurl.sourceforge.net/download/pycurl-%{version}.tar.gz
%define sha1    pycurl=60865d22fc715ca5197117ea3ad32413d3c7402e
Vendor:         VMware, Inc.
Distribution:   Photon
Provides:       pycurl
Requires:       python2
BuildRequires:  openssl-devel
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  curl
Requires:       curl
%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%package -n     pycurl3
Summary:        python3 pycurl
BuildRequires:  openssl-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs
Requires:       curl

%description -n pycurl3
Python 3 version.

%package        doc
Summary:        Documentation and examples for pycurl
Requires:       %{name} = %{version}

%description    doc
Documentation and examples for pycurl

%prep
%setup -q -n pycurl-%{version}
rm -f doc/*.xml_validity
#chmod a-x examples/*

# removing prebuilt-binaries
rm -f tests/fake-curl/libcurl/*.so
rm -rf ../p3dir
cp -a . ../p3dir

%build
CFLAGS="$RPM_OPT_FLAGS -DHAVE_CURL_OPENSSL" python2 setup.py build
pushd ../p3dir
CFLAGS="$RPM_OPT_FLAGS -DHAVE_CURL_OPENSSL" python3 setup.py build
popd

%install
rm -rf %{buildroot}
python2 setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/pycurl
chmod 755 %{buildroot}%{python2_sitelib}/pycurl.so
pushd ../p3dir
python3 setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{_datadir}/doc/pycurl
chmod 755 %{buildroot}%{python3_sitelib}/pycurl*.so
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n pycurl3
%defattr(-,root,root,-)
%{python3_sitelib}/*

%files doc
%defattr(-,root,root)
%doc COPYING-LGPL COPYING-MIT RELEASE-NOTES.rst ChangeLog README.rst examples doc tests

%changelog
*   Fri Jun 02 2017 Xiaolin Li <xiaolinl@vmware.com> 7.21.5-4
-   Add pycurl3.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.21.5-3
-   GA - Bump release of all rpms
*   Fri Apr 29 2016 Divya Thaluru <dthaluru@vmware.com> 7.21.5-2
-   Removing prebuilt binaries
*   Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 7.21.5-1
-   Upgrade version
*   Mon Jul 6 2015 Alexey Makhalov <amakhalov@vmware.com> 7.19.5.1-2
-   Added Doc subpackage. Removed chmod a-x for examples.
*   Sat Jan 24 2015 Touseef Liaqat <tliaqat@vmware.com> 7.19.5.1
-   Initial build.  First version
