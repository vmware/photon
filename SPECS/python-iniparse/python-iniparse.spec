%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-iniparse
Version:        0.4
Release:        4%{?dist}
Summary:        Python Module for Accessing and Modifying Configuration Data in INI files
Group:          Development/Libraries
License:        MIT
URL:            http://code.google.com/p/iniparse/
Source0:        http://iniparse.googlecode.com/files/iniparse-%{version}.tar.gz
%define sha1 iniparse=2b2af8a19f3e5c212c27d7c524cd748fa0b38650
Vendor:		VMware, Inc.
Distribution:	Photon
BuildRequires:	python2-devel
BuildRequires:	python2-libs
BuildArch:	noarch
Requires:	python2

%description
iniparse is an INI parser for Python which is API compatible
with the standard library's ConfigParser, preserves structure of INI
files (order of sections & options, indentation, comments, and blank
lines are preserved when data is updated), and is more convenient to
use.

%package -n     python3-iniparse
Summary:        python-iniparse
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-iniparse
Python 3 version.

%prep
%setup -q -n iniparse-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
rm -rf $RPM_BUILD_ROOT
python2 setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
# fixes
chmod 644 $RPM_BUILD_ROOT/usr/share/doc/iniparse-%{version}/index.html
mv $RPM_BUILD_ROOT/usr/share/doc/iniparse-%{version} $RPM_BUILD_ROOT/usr/share/doc/python-iniparse-%{version}
pushd ../p3dir
python3 setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
# fixes
chmod 644 $RPM_BUILD_ROOT/usr/share/doc/iniparse-%{version}/index.html
mv $RPM_BUILD_ROOT/usr/share/doc/iniparse-%{version} $RPM_BUILD_ROOT/usr/share/doc/python3-iniparse-%{version}
popd


%check
cp -r iniparse/ tests/
cd tests
python2 test_misc.py
python2 test_tidy.py
python2 test_fuzz.py
python2 test_ini.py
python2 test_multiprocessing.py
python2 test_unicode.py
pushd ../p3dir
cp -r iniparse/ tests/
cd tests
python3 test_misc.py
python3 test_tidy.py
python3 test_fuzz.py
python3 test_ini.py
python3 test_multiprocessing.py
python3 test_unicode.py
popd


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc  %{_docdir}/python-iniparse-%{version}/*
%{python2_sitelib}/iniparse
%{python2_sitelib}/iniparse-%{version}-py*.egg-info


%files -n python3-iniparse
%defattr(-,root,root,-)
%doc  %{_docdir}/python3-iniparse-%{version}/*
%{python3_sitelib}/iniparse
%{python3_sitelib}/iniparse-%{version}-py*.egg-info

%changelog
*       Mon Apr 10 2017 Sarah Choi <sarahc@vmware.com> 0.4-4
-       Support python3
*       Mon Oct 03 2016 ChangLee <changLee@vmware.com> 0.4-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.4-2
-	GA - Bump release of all rpms
