Summary:        Interface for Python to call C code
Name:           python-cffi
Version:        1.3.0
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/cffi
License:        MIT
Group:          Development/Languages/Python
Source0:        https://pypi.python.org/packages/source/c/cffi/cffi-1.3.0.tar.gz
%define sha1 cffi=54a0b2dbbc2f5d99131aa337e217b636652641a9

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: libffi
BuildRequires:  python-pycparser
Requires:       python2
Requires:		python2-libs
Requires:       python-pycparser

BuildArch:      x86_64

%description
Foreign Function Interface for Python, providing a convenient and reliable way of calling existing C code from Python. The interface is based on LuaJIT’s FFI.

%prep
%setup -q -n cffi-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/*

%changelog
* Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.3.0-1
- Initial packaging for Photon
