%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary: Download, build, install, upgrade, and uninstall Python packages
Name: python-setuptools
Version: 34.3.3
Release: 2%{?dist}
License: Python or ZPLv2.0
Group: Development/Languages
Vendor: VMware, Inc.
Distribution: Photon
URL: https://pypi.python.org/pypi/setuptools

Source0: https://pypi.python.org/packages/d5/b7/e52b7dccd3f91eec858309dcd931c1387bf70b6d458c86a9bfcb50134fbd/setuptools-%{version}.zip
%define sha1 setuptools=0cc980f018b539f1f87ef3e09849e5f4d1bd9a5d

BuildArch: noarch

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: unzip
BuildRequires: python-six
BuildRequires: python-packaging
BuildRequires: python-appdirs
BuildRequires: python-pyparsing

Requires: python2
Requires: python2-libs
Requires: python-six
Requires: python-packaging
Requires: python-appdirs
Requires: python-pyparsing

%description
setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

%prep
%setup -n setuptools-%{version}

%build
python2 setup.py build

%install
%{__rm} -rf %{buildroot}
python2 setup.py install -O1 --skip-build \
    --root "%{buildroot}" \
    --single-version-externally-managed
find %{buildroot}%{python2_sitelib} -name '*.exe' | xargs rm -f
find %{buildroot}%{python2_sitelib} -name '*.txt' | xargs chmod -x
chmod +x %{buildroot}%{python2_sitelib}/setuptools/command/easy_install.py

%check
python2 setup.py test

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%{_bindir}/*
%{python2_sitelib}/*

%changelog
*       Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 34.3.3-2
-       Use python2 explicitly and add Vendor
*       Mon Apr 03 2017 Sarah Choi <sarahc@vmware.com> 34.3.3-1
-       Upgrade to 34.3.3
*       Mon Oct 10 2016 ChangLee <changlee@vmware.com> 21.0.0-3
-       Modified %check
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 21.0.0-2
-	GA - Bump release of all rpms
*	Wed May 4 2016 Xiaolin Li <xiaolinl@vmware.com> 21.0.0-1
-	Update setuptools to version 21.0.0
* Wed Feb 11 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
