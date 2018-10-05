%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A XML/HTML/XHTML Markup safe string for Python.
Name:           python-markupsafe
Version:        1.0
Release:        3%{?dist}
License:        BSD
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
URL:            https://pypi.python.org/pypi/MarkupSafe
Source0:        https://pypi.python.org/packages/4d/de/32d741db316d8fdb7680822dd37001ef7a448255de9699ab4bfcbdf4172b/MarkupSafe-%{version}.tar.gz
%define sha1    MarkupSafe=9072e80a7faa0f49805737a48f3d871eb1c48728

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python2
Requires:       python2-libs

%description
MarkupSafe implements a XML/HTML/XHTML Markup safe string for Python.

%package -n     python3-markupsafe
Summary:        python-markupsafe
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
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.0-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.0-2
-   Removed erroneous version line
*   Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 1.0-1
-   Upgrade version to 1.0
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 0.23-1
-   Initial packaging for Photon
