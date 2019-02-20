%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Pygments is a syntax highlighting package written in Python.
Name:           python-Pygments
Version:        2.3.1
Release:        1%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/Pygments
Source0:        https://files.pythonhosted.org/packages/source/P/Pygments/Pygments-%{version}.tar.gz
%define         sha1 Pygments=88f8da2d10cb21362a9e04b154932892c2695670

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
Pygments is a syntax highlighting package written in Python.

It is a generic syntax highlighter suitable for use in code hosting, forums, wikis or other applications that need to prettify source code. Highlights are:

a wide range of over 300 languages and other text formats is supported
special attention is paid to details, increasing quality by a fair amount
support for new languages and formats are added easily
a number of output formats, presently HTML, LaTeX, RTF, SVG, all image formats that PIL supports and ANSI sequences
it is usable as a command-line tool and as a library.

%package -n     python3-Pygments
Summary:        python-Pygments
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-Pygments
Python 3 version.

%prep
%setup -q -n Pygments-%{version}
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

%files -n python3-Pygments
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/*

%changelog
*   Wed Feb 20 2019 Dweep Advani <dadvani@vmware.com> 2.3.1-1
-   Upgraded to version 2.3.1
*   Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 2.2.0-1
-   Initial packaging for Photon
