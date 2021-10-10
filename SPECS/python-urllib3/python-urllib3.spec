%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        A powerful, sanity-friendly HTTP client for Python.
Name:           python-urllib3
Version:        1.26.6
Release:        1%{?dist}
Url:            https://pypi.python.org/pypi/urllib3
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://github.com/shazow/urllib3/archive/urllib3-1.26.6.tar.gz
%define sha1    urllib3=5b1d645e121049efe19066388b2a42319096a93f

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
urllib3 is a powerful, sanity-friendly HTTP client for Python. Much of the Python ecosystem already uses urllib3 and you should too.

%package -n     python3-urllib3
Summary:        python-urllib3
Requires:       python3
Requires:       python3-libs

%description -n python3-urllib3
Python 3 version.

%prep
%setup -q -n urllib3-%{version}

%build
python setup.py build
python3 setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python setup.py test
python3 setup.py test

%files
%defattr(-,root,root)
%{python_sitelib}/*

%files -n python3-urllib3
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sun Oct 10 2021 Shreyas B <shreyasb@vmware.com> 1.26.6-1
-   Upgrade to v1.26.6
*   Thu Feb 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.20-1
-   Initial packaging for Photon
