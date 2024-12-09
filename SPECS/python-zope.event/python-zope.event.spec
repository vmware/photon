Name:           python3-zope.event
Version:        4.5.0
Release:        3%{?dist}
Summary:        Very basic event publishing system
Group:          Development/Libraries/Python
Url:            http://pypi.python.org/pypi/zope.event
Source0:        https://pypi.python.org/packages/source/z/zope.event/zope.event-%{version}.tar.gz
%define sha512  zope.event=1d82ae316fc75eebc03aadeb78890a19add35490720cd7bd073faeb9dc9ed97511ca4fdafc2228530798384d667c0aa88e3ef47b0be668128556a78bf82c42e5

Source1: license.txt
%include %{SOURCE1}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
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
%autosetup -n zope.event-%{version}

%build
%py3_build

%install
%py3_install

%check
python setup.py test

%files
%defattr(-,root,root)
%doc CHANGES.rst COPYRIGHT.txt LICENSE.txt README.rst
%{python3_sitelib}/*

%changelog
* Wed Dec 11 2024 Prashant S Chauhan <prashant.singh-chauhan@broadcom.com> 4.5.0-3
- Release bump for SRP compliance
* Fri Dec 02 2022 Prashant S Chauhan <psinghchauha@vmware.com> 4.5.0-2
- Update release to compile with python 3.11
* Tue Feb 23 2021 Tapas Kundu <tkundu@vmware.com> 4.5.0-1
- Initial build.  First version
