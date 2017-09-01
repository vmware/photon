%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-docopt
Version:        0.6.2
Release:        1%{?dist}
Summary:        Pythonic argument parser to create command line interfaces.
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/docopt
Source0:        docopt-%{version}.tar.gz
%define sha1    docopt=224a3ec08b56445a1bd1583aad06b00692671e04
Vendor:         VMware, Inc.
Distribution:   Photon

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python-pytest
Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools

BuildArch:      noarch

%description
docopt helps easily create most beautiful command-line interfaces.

%package -n     python3-docopt
Summary:        python-docopt
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pytest
Requires:       python3
Requires:       python3-libs
Requires:       python3-setuptools

%description -n python3-docopt
Python 3 version.

%prep
%setup -n docopt-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%files -n python3-docopt
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.6.2-1
-   Initial version of python-docopt package for Photon.
