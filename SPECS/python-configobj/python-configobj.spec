Name:           python-configobj
Version:        5.0.6
Release:        2%{?dist}
Summary:        Config file reading, writing and validation
License:        BSD
Group:          Development/Languages/Python
Url:            https://pypi.python.org/packages/source/c/configobj/configobj-%{version}.tar.gz
Source0:        configobj-%{version}.tar.gz
%define sha1 configobj=add3ae15e3f0d2d28d37370dcad930243cb4145c

BuildRequires: python2
BuildRequires: python2-libs
BuildRequires: python-setuptools

Requires: python-six

BuildArch:      noarch

%description
ConfigObj is a simple but powerful config file reader and writer: an ini file round tripper. Its main feature is that it is very easy to use, with a straightforward programmer’s interface and a simple syntax for config files.

%prep
%setup -n configobj-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python validate.py

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 5.0.6-2
-	GA - Bump release of all rpms
* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
