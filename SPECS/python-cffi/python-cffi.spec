Summary:        Interface for Python to call C code
Name:           python-cffi
Version:        1.5.2
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/cffi
License:        MIT
Group:          Development/Languages/Python
Source0:        https://pypi.python.org/packages/source/c/cffi/cffi-%{version}.tar.gz
%define sha1 cffi=5239b3aa4f67eed3559c09778096ecd4faeca876

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: libffi
BuildRequires:  python-pycparser
Requires:       python2
Requires:       python2-libs
Requires:       python-pycparser

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
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5.2-2
-	GA - Bump release of all rpms
*   Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.5.2-1
-   Updated to version 1.5.2
*	Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.5.0-1
-	Upgrade version
* 	Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.3.0-1
- 	nitial packaging for Photon
