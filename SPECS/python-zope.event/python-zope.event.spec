Name:           python3-zope.event
Version:        4.5.0
Release:        3%{?dist}
Summary:        Very basic event publishing system
License:        ZPL-2.1
Group:          Development/Libraries/Python
URL:            http://pypi.python.org/pypi/zope.event
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: https://pypi.python.org/packages/source/z/zope.event/zope.event-%{version}.tar.gz
%define sha512 zope.event=1d82ae316fc75eebc03aadeb78890a19add35490720cd7bd073faeb9dc9ed97511ca4fdafc2228530798384d667c0aa88e3ef47b0be668128556a78bf82c42e5

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-sphinx

Requires: python3
Requires: python3-setuptools
Requires: python3-sphinx

BuildArch: noarch

%description
An event publishing system and a very simple event-dispatching system on
which more sophisticated event dispatching systems can be built. For
example, a type-based event dispatching system that builds on zope.event
can be found in zope.component.

%prep
%autosetup -n zope.event-%{version}

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
* Mon Jan 08 2024 Nitesh Kumar <kunitesh@vmware.com> 4.5.0-3
- Version bump up as a part of python3-sphinx upgrade v5.1.1
* Thu Dec 09 2021 Prashant S Chauhan <psinghchauha@vmware.com> 4.5.0-2
- Bump up to compile with python 3.10
* Tue Feb 23 2021 Tapas Kundu <tkundu@vmware.com> 4.5.0-1
- Initial build.  First version
