Name:           python-pyasn1
Version:        0.1.7
Release:        1
Summary:        Implementation of ASN.1 types and codecs in Python programming language
License:        BSD
Group:          Development/Languages/Python
Url:            https://pypi.python.org/packages/source/p/pyasn1/pyasn1-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python-setuptools

Requires: python2
Requires: python2-libs

BuildArch:      noarch

%description
This is an implementation of ASN.1 types and codecs in Python programming language. It has been first written to support particular protocol (SNMP) but then generalized to be suitable for a wide range of protocols based on ASN.1 specification.

%prep
%setup -n %{name}-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
* Fri Mar 13 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Discus
