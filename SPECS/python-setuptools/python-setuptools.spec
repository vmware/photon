%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:       Download, build, install, upgrade, and uninstall Python packages
Name:          python-setuptools
Version:       34.3.3
Release:       2%{?dist}
License:       Python or ZPLv2.0
Group:         Development/Languages
URL:           https://pypi.python.org/pypi/setuptools

Source0:       https://pypi.python.org/packages/d5/b7/e52b7dccd3f91eec858309dcd931c1387bf70b6d458c86a9bfcb50134fbd/setuptools-%{version}.zip
%define sha1 setuptools=0cc980f018b539f1f87ef3e09849e5f4d1bd9a5d

BuildArch:     noarch

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: unzip
BuildRequires: python-six
BuildRequires: python-packaging
BuildRequires: python-appdirs
BuildRequires: python-pyparsing

Requires:      python2
Requires:      python2-libs
Requires:      python-six
Requires:      python-packaging
Requires:      python-appdirs
Requires:      python-pyparsing

%description
setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

%package -n     python3-setuptools
Summary:        Python 3 version

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  unzip
BuildRequires:  python3-six
BuildRequires:  python3-packaging
BuildRequires:  python3-appdirs
BuildRequires:  python3-pyparsing

Requires:       python3
Requires:       python3-libs
Requires:       python3-six
Requires:       python3-packaging
Requires:       python3-appdirs
Requires:       python3-pyparsing

%description -n python3-setuptools
Python3 version.

%prep
%setup -n setuptools-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
%{__rm} -rf %{buildroot}
python2 setup.py install -O1 --skip-build --root "%{buildroot}" --single-version-externally-managed
find %{buildroot}%{python2_sitelib} -name '*.exe' | xargs rm -f
find %{buildroot}%{python2_sitelib} -name '*.txt' | xargs chmod -x
chmod +x %{buildroot}%{python2_sitelib}/setuptools/command/easy_install.py

pushd ../p3dir
python3 setup.py install -O1 --skip-build --root "%{buildroot}" --single-version-externally-managed
find %{buildroot}%{python3_sitelib} -name '*.exe' | xargs rm -f
find %{buildroot}%{python3_sitelib} -name '*.txt' | xargs chmod -x
chmod +x %{buildroot}%{python3_sitelib}/setuptools/command/easy_install.py
popd

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root)
%{_bindir}/*
%{python2_sitelib}/*

%files -n python3-setuptools
%defattr(-,root,root,-)
%{_bindir}/*
%{python3_sitelib}/*

%changelog
*    Mon May 15 2017 Kumar Kaushik <kaushikk@vmware.com> 34.3.3-2
-    Adding python 3 support
*    Mon Apr 03 2017 Sarah Choi <sarahc@vmware.com> 34.3.3-1
-    Upgrade to 34.3.3
*    Mon Oct 10 2016 ChangLee <changlee@vmware.com> 21.0.0-3
-    Modified %check
*    Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 21.0.0-2
-    GA - Bump release of all rpms
*    Wed May 4 2016 Xiaolin Li <xiaolinl@vmware.com> 21.0.0-1
-    Update setuptools to version 21.0.0
*    Wed Feb 11 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
-    Initial packaging for Photon
