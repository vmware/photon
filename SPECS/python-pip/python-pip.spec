# FIXME: noarch or generate debuginfo
%define debug_package %{nil}

Name:           python-pip
Version:        8.1.2
Release:        3%{?dist}
Url:            https://pypi.python.org/pypi/pip
Summary:        The PyPA recommended tool for installing Python packages.
License:        MIT
Group:          Development/Languages/Python
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14aeff0acb03c64707ce100ecd53934da1aa13/pip-%{version}.tar.gz
%define sha1 pip=910e2dd5c533d351a7dc84bc9091893659afcbb0
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs
Requires:       python-setuptools
Requires:       python-xml

%description
The PyPA recommended tool for installing Python packages.


%prep
%setup -q -n pip-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install freezegun
%{__python} setup.py test

%files
%defattr(-,root,root)
%{python_sitelib}/*
%{_bindir}/*

%changelog
*   Wed Jul 12 2017 Xiaolin Li <xiaolinl@vmware.com> 8.1.2-3
-   Added python-xml to requires.
*   Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 8.1.2-2
-   Added python-setuptools to requires.
*   Fri Sep 2 2016 Xiaolin Li <xiaolinl@vmware.com> 8.1.2-1
-   Initial packaging for Photon
