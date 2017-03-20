%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Docutils -- Python Documentation Utilities.
Name:           python-docutils
Version:        0.13.1
Release:        1%{?dist}
License:        public domain, Python, 2-Clause BSD, GPL 3 (see COPYING.txt)
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/docutils
Source0:        https://files.pythonhosted.org/packages/source/d/docutils/docutils-%{version}.tar.gz
%define         sha1 docutils=c16e14ef18142fa248400cd174edb4fa40e51d5b

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
Docutils is a modular system for processing documentation into useful formats, such as HTML, XML, and LaTeX. For input Docutils supports reStructuredText, an easy-to-read, what-you-see-is-what-you-get plaintext markup syntax.

%package -n     python3-docutils
Summary:        python-docutils
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python3
Requires:       python3-libs

%description -n python3-docutils
Python 3 version.

%prep
%setup -q -n docutils-%{version}
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

%files
%defattr(-,root,root)
%{python2_sitelib}/*

%files -n python3-docutils
%defattr(-,root,root)
%{python3_sitelib}/*
%{_bindir}/*

%changelog
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 0.13.1-1
-   Initial packaging for Photon
