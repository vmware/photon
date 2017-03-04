%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        A XML/HTML/XHTML Markup safe string for Python.
Name:           python-markupsafe
Version:        0.23
Release:        1%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Url:            https://pypi.python.org/pypi/MarkupSafe
Source0:        MarkupSafe-%{version}.tar.gz
%define sha1    MarkupSafe=cd5c22acf6dd69046d6cb6a3920d84ea66bdf62a

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

%description
MarkupSafe implements a XML/HTML/XHTML Markup safe string for Python.

%package -n     python3-markupsafe
Summary:        python-markupsafe
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs

%description -n python3-markupsafe
Python 3 version.

%prep
%setup -q -n MarkupSafe-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install py
python2 setup.py test
python3 setup.py test

%files
%defattr(-,root,root,-)
%{python2_sitelib}/*

%files -n python3-markupsafe
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 0.23-1
-   Initial packaging for Photon
