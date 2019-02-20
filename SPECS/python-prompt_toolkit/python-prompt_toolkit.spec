%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Library for building powerful interactive command lines in Python.
Name:           python-prompt_toolkit
Version:        2.0.8
Release:        1%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/prompt_toolkit
Source0:        https://files.pythonhosted.org/packages/source/p/prompt_toolkit/prompt_toolkit-%{version}.tar.gz
%define         sha1 prompt_toolkit=173350aa955e6b0d82363c25ed94eb151a39863b

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
prompt_toolkit is a library for building powerful interactive command lines and terminal applications in Python.

%package -n     python3-prompt_toolkit
Summary:        python-prompt_toolkit
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-prompt_toolkit
Python 3 version.

%prep
%setup -q -n prompt_toolkit-%{version}
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

%files -n python3-prompt_toolkit
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
*   Wed Feb 20 2019 Dweep Advani <dadvani@vmware.com> 2.0.8-1
-   Upgraded to version 2.0.8
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0.14-1
-   Initial packaging for Photon
