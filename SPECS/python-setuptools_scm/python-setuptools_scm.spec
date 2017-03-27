%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        the blessed package to manage your versions by scm tags.
Name:           python-setuptools_scm
Version:        1.15.0
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/setuptools_scm
Source0:        https://files.pythonhosted.org/packages/source/s/setuptools_scm/setuptools_scm-%{version}.tar.gz
%define         sha1 setuptools_scm=273bb9fbc27d169cb9853b379db8f749ea7caede

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
setuptools_scm handles managing your python package versions in scm metadata instead of declaring them as the version argument or in a scm managed file.

It also handles file finders for the supported scm’s.

%package -n     python3-setuptools_scm
Summary:        python-setuptools_scm
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-setuptools_scm
Python 3 version.

%prep
%setup -q -n setuptools_scm-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-setuptools_scm
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-1
-   Initial packaging for Photon
