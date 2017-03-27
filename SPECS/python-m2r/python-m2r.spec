%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Markdown to reStructuredText converter.
Name:           python-m2r
Version:        0.1.5
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/m2r
Source0:        https://files.pythonhosted.org/packages/source/m/m2r/m2r-%{version}.tar.gz
%define         sha1 m2r=9c5aa6fa791ff53c5007774159d4d0d2ffb4e36a

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
M2R converts a markdown file including reST markups to a valid reST format.

Why another converter?

I wanted to write sphinx document in markdown, since it’s widely used now and easy to write code blocks and lists. However, converters using pandoc or recommonmark do not support many reST markups and sphinx extensions. For example, reST’s reference link like see `ref`_ (this is very convenient in long document in which same link appears multiple times) will be converted to a code block in HTML like see <code>ref</code>_, which is not expected.

%package -n     python3-m2r
Summary:        python-m2r
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-m2r
Python 3 version.

%prep
%setup -q -n m2r-%{version}
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

%files -n python3-m2r
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/*

%changelog
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.1.5-1
-   Initial packaging for Photon
