Summary:        Python C parser
Name:           python-pycparser
Version:        2.14
Release:        2%{?dist}
Url:            https://pypi.python.org/pypi/pycparser
License:        BSD
Group:          Development/Languages/Python
Source0:        https://pypi.python.org/packages/source/p/pycparser/pycparser-2.14.tar.gz
%define sha1 pycparser=922162bad4aa8503988035506c1c65bbf8690ba4

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python2-devel
BuildRequires: python-setuptools

Requires:       python2
Requires:       python2-libs


%description
pycparser is a complete parser of the C language, written in pure Python using the PLY parsing library. It parses C code into an AST and can serve as a front-end for C compilers or analysis tools. 

%prep
%setup -q -n pycparser-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root)
%{python_sitelib}/*


%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.14-2
-	GA - Bump release of all rpms
* Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> 2.14-1
- Initial packaging for Photon
