Name:           python-jinja2
Version:        2.8
Release:        1%{?dist}
Url:            http://jinja.pocoo.org/
Summary:        A fast and easy to use template engine written in pure Python
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://pypi.python.org/packages/source/J/Jinja2/Jinja2-%{version}.tar.gz
%define sha1 Jinja2=4a33c1a0fd585eba2507e8c274a9cd113b1d13ab
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
Jinja2 is a template engine written in pure Python.  It provides a Django
inspired non-XML syntax but supports inline expressions and an optional
sandboxed environment.

%prep
%setup -q -n Jinja2-%{version}

%build
python setup.py build
sed -i 's/\r$//' LICENSE # Fix wrong EOL encoding

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root)
%doc AUTHORS CHANGES
%license LICENSE
%{python_sitelib}/jinja2
%exclude %{python_sitelib}/*/*.py
%{python_sitelib}/Jinja2-%{version}-py%{python_version}.egg-info

%changelog
*   Tue Dec 13 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.8-1
-   Initial packaging for Photon
