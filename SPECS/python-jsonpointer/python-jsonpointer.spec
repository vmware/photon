Name:           python-jsonpointer
Version:        1.7
Release:        1
Summary:        Applying JSON Patches in Python
License:        Modified BSD License
Group:          Development/Languages/Python
Url:            https://pypi.python.org/packages/source/j/jsonpointer/jsonpointer-%{version}.tar.gz
Source0:        jsonpointer-%{version}.tar.gz

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python-setuptools

Requires: python2
Requires: python2-libs

BuildArch:      noarch

%description
Library to apply JSON Patches according to RFC 6902.

%prep
%setup -n jsonpointer-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%{_bindir}/jsonpointer

%changelog
* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon