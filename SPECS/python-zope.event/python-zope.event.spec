%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python3-zope.event
Version:        4.5.0
Release:        1%{?dist}
Summary:        Very basic event publishing system
License:        ZPL-2.1
Group:          Development/Libraries/Python
Url:            http://pypi.python.org/pypi/zope.event
Source0:        https://pypi.python.org/packages/source/z/zope.event/zope.event-%{version}.tar.gz
%define sha1    zope.event=32ac2c3f2c4c9bb6f4d7bccbb5dbd6f22964d6ad
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3
BuildRequires:  python3-sphinx
Requires:       python3
Requires:       python3-setuptools
Requires:       python3-sphinx
BuildArch:      noarch
Vendor:         VMware, Inc.
Distribution:   Photon

%description
An event publishing system and a very simple event-dispatching system on
which more sophisticated event dispatching systems can be built. For
example, a type-based event dispatching system that builds on zope.event
can be found in zope.component.

%prep
%setup -q -n zope.event-%{version}

%build
python setup.py build

%install
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python setup.py test

%files
%defattr(-,root,root)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{python3_sitelib}/*

%changelog
*   Tue Feb 23 2021 Tapas Kundu <tkundu@vmware.com> 4.5.0-1
-   Initial build.  First version
